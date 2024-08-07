from icu import Locale, BreakIterator


import sys
import six
from six import text_type as unicode

from functools import cached_property

string_types = (str,)
basestring = (str, bytes)
implements_to_string = lambda x: x

class ComparableMixin(object):

    '''Implements rich operators for an object.'''

    def _compare(self, other, method):
        try:
            return method(self._cmpkey(), other._cmpkey())
        except (AttributeError, TypeError):
            # _cmpkey not implemented, or return different type,
            # so I can't compare with "other". Try the reverse comparison
            return NotImplemented

    def __lt__(self, other):
        return self._compare(other, lambda s, o: s < o)

    def __le__(self, other):
        return self._compare(other, lambda s, o: s <= o)

    def __eq__(self, other):
        return self._compare(other, lambda s, o: s == o)

    def __ge__(self, other):
        return self._compare(other, lambda s, o: s >= o)

    def __gt__(self, other):
        return self._compare(other, lambda s, o: s > o)

    def __ne__(self, other):
        return self._compare(other, lambda s, o: s != o)


class BlobComparableMixin(ComparableMixin):

    '''Allow blob objects to be comparable with both strings and blobs.'''

    def _compare(self, other, method):
        if isinstance(other, basestring):
            # Just compare with the other string
            return method(self._cmpkey(), other)
        return super(BlobComparableMixin, self)._compare(other, method)

@implements_to_string
class StringlikeMixin(object):

    '''Make blob objects behave like Python strings.

    Expects that classes that use this mixin to have a _strkey() method that
    returns the string to apply string methods to. Using _strkey() instead
    of __str__ ensures consistent behavior between Python 2 and 3.
    '''

    def __repr__(self):
        '''Returns a string representation for debugging.'''
        class_name = self.__class__.__name__
        text = str(self)
        ret = '{cls}("{text}")'.format(cls=class_name,
                                        text=text)
        return ret

    def __str__(self):
        '''Returns a string representation used in print statements
        or str(my_blob).'''
        return self._strkey()

    def __len__(self):
        '''Returns the length of the raw text.'''
        return len(self._strkey())

    def __iter__(self):
        '''Makes the object iterable as if it were a string,
        iterating through the raw string's characters.
        '''
        return iter(self._strkey())

    def __contains__(self, sub):
        '''Implements the `in` keyword like a Python string.'''
        return sub in self._strkey()

    def __getitem__(self, index):
        '''Returns a  substring. If index is an integer, returns a Python
        string of a single character. If a range is given, e.g. `blob[3:5]`,
        a new instance of the class is returned.
        '''
        if isinstance(index, int):
            return self._strkey()[index]  # Just return a single character
        else:
            # Return a new blob object
            return self.__class__(self._strkey()[index])

    def find(self, sub, start=0, end=sys.maxsize):
        '''Behaves like the built-in str.find() method. Returns an integer,
        the index of the first occurrence of the substring argument sub in the
        sub-string given by [start:end].
        '''
        return self._strkey().find(sub, start, end)

    def rfind(self, sub, start=0, end=sys.maxsize):
        '''Behaves like the built-in str.rfind() method. Returns an integer,
        the index of he last (right-most) occurence of the substring argument
        sub in the sub-sequence given by [start:end].
        '''
        return self._strkey().rfind(sub, start, end)

    def index(self, sub, start=0, end=sys.maxsize):
        '''Like blob.find() but raise ValueError when the substring
        is not found.
        '''
        return self._strkey().index(sub, start, end)

    def rindex(self, sub, start=0, end=sys.maxsize):
        '''Like blob.rfind() but raise ValueError when substring is not
        found.
        '''
        return self._strkey().rindex(sub, start, end)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        """Returns True if the blob starts with the given prefix."""
        return self._strkey().startswith(prefix, start, end)

    def endswith(self, suffix, start=0, end=sys.maxsize):
        """Returns True if the blob ends with the given suffix."""
        return self._strkey().endswith(suffix, start, end)

    # PEP8 aliases
    starts_with = startswith
    ends_with = endswith

    def title(self):
        """Returns a blob object with the text in title-case."""
        return self.__class__(self._strkey().title())

    def format(self, *args, **kwargs):
        """Perform a string formatting operation, like the built-in
        `str.format(*args, **kwargs)`. Returns a blob object.
        """
        return self.__class__(self._strkey().format(*args, **kwargs))

    def split(self, sep=None, maxsplit=sys.maxsize):
        """Behaves like the built-in str.split().
        """
        return self._strkey().split(sep, maxsplit)

    def strip(self, chars=None):
        """Behaves like the built-in str.strip([chars]) method. Returns
        an object with leading and trailing whitespace removed.
        """
        return self.__class__(self._strkey().strip(chars))

    def upper(self):
        """Like str.upper(), returns new object with all upper-cased characters.
        """
        return self.__class__(self._strkey().upper())

    def lower(self):
        """Like str.lower(), returns new object with all lower-cased characters.
        """
        return self.__class__(self._strkey().lower())

    def join(self, iterable):
        """Behaves like the built-in `str.join(iterable)` method, except
        returns a blob object.

        Returns a blob which is the concatenation of the strings or blobs
        in the iterable.
        """
        return self.__class__(self._strkey().join(iterable))

    def replace(self, old, new, count=sys.maxsize):
        """Return a new blob object with all the occurence of `old` replaced
        by `new`.
        """
        return self.__class__(self._strkey().replace(old, new, count))


class Word(unicode):

  """A simple word representation. Includes methods for inflection,
  translation, and WordNet integration.
  """

  def __new__(cls, string, language=None, pos_tag=None):
    """Return a new instance of the class. It is necessary to override
    this method in order to handle the extra pos_tag argument in the
    constructor.
    """
    return super(Word, cls).__new__(cls, string)

  def __init__(self, string, language=None, pos_tag=None):
    self.string = string
    self.pos_tag = pos_tag
    self.__lang = language

  def __repr__(self):
      return repr(self.string)

  def __str__(self):
    return self.string

  @property
  def language(self):
    if self.__lang is None:
      self.__lang = self.detected_languages.language.code
    return self.__lang

  @language.setter
  def language(self, value):
    self.__lang = value


class WordList(list):
  """A list-like collection of words."""

  def __init__(self, collection, parent=None, language="en"):
    """Initialize a WordList. Takes a collection of strings as
    its only argument.
    """
    self._collection = [Word(w, language=language) for w in collection]
    self.parent = parent
    super(WordList, self).__init__(self._collection)

  def __str__(self):
    return str(self._collection)

  def __repr__(self):
    """Returns a string representation for debugging."""
    class_name = self.__class__.__name__
    return '{cls}({lst})'.format(cls=class_name, lst=repr(self._collection))

  def __getitem__(self, key):
    """Returns a string at the given index."""
    if isinstance(key, slice):
        return self.__class__(self._collection[key])
    else:
        return self._collection[key]

  def __getslice__(self, i, j):
    # This is included for Python 2.* compatibility
    return self.__class__(self._collection[i:j])

  def __iter__(self):
    return iter(self._collection)

  def count(self, strg, case_sensitive=False, *args, **kwargs):
    """Get the count of a word or phrase `s` within this WordList.
    :param strg: The string to count.
    :param case_sensitive: A boolean, whether or not the search is case-sensitive.
    """
    if not case_sensitive:
        return [word.lower() for word in self].count(strg.lower(), *args,
                **kwargs)
    return self._collection.count(strg, *args, **kwargs)

  def append(self, obj):
    """Append an object to end. If the object is a string, appends a
    :class:`Word <Word>` object.
    """
    if isinstance(obj, basestring):
        return self._collection.append(Word(obj))
    else:
        return self._collection.append(obj)

  def extend(self, iterable):
    """Extend WordList by appending elements from ``iterable``. If an element
    is a string, appends a :class:`Word <Word>` object.
    """
    [self._collection.append(Word(e) if isinstance(e, basestring) else e)
        for e in iterable]
    return self

  def upper(self):
    """Return a new WordList with each word upper-cased."""
    return self.__class__([word.upper() for word in self])

  def lower(self):
    """Return a new WordList with each word lower-cased."""
    return self.__class__([word.lower() for word in self])


class BaseBlob(StringlikeMixin, BlobComparableMixin):
  """An abstract base class that Sentence, Text will inherit from.
  Includes words, POS tag, NP, and word count properties. Also includes
  basic dunder and string methods for making objects like Python strings.
  :param text: A string.
  """

  def __init__(self, text):
    self.hint_language_code = None


  @property
  def word_tokenizer(self):
    word_tokenizer = WordTokenizer(locale=self.language.code)
    return word_tokenizer

  @property
  def words(self):
    """Return a list of word tokens. This is an alias for the ``tokens``
    property.
    :returns: A :class:`WordList <WordList>` of word tokens.
    """
    return self.tokens

  @cached_property
  def tokens(self):
    """Return a list of tokens, using this blob's tokenizer object
    (defaults to :class:`WordTokenizer <textblob.tokenizers.WordTokenizer>`).
    """
    seq = self.word_tokenizer.transform(Sequence(self.raw))
    return WordList(seq.tokens(), parent=self, language=self.language.code)

  def tokenize(self, tokenizer=None):
    """Return a list of tokens, using ``tokenizer``.
    :param tokenizer: (optional) A tokenizer object. If None, defaults to
        this blob's default tokenizer.
    """
    t = tokenizer if tokenizer is not None else self.tokenizer
    return WordList(t.tokenize(self.raw), parent=self)

  def _cmpkey(self):
    """Key used by ComparableMixin to implement all rich comparison
    operators.
    """
    return self.raw

  def _strkey(self):
    """Key used by StringlikeMixin to implement string methods."""
    return self.raw

  def __hash__(self):
    return hash(self._cmpkey())

  def __add__(self, other):
    '''Concatenates two text objects the same way Python strings are
    concatenated.
    Arguments:
    - `other`: a string or a text object
    '''
    if isinstance(other, basestring):
        return self.__class__(self.raw + other)
    elif isinstance(other, BaseBlob):
        return self.__class__(self.raw + other.raw)
    else:
        raise TypeError('Operands must be either strings or {0} objects'
            .format(self.__class__.__name__))

  def split(self, sep=None, maxsplit=sys.maxsize):
    """Behaves like the built-in str.split() except returns a
    WordList.
    :rtype: :class:`WordList <WordList>`
    """
    return WordList(self._strkey().split(sep, maxsplit), parent=self)
  

class Text(BaseBlob):

  def __init__(self, text, hint_language_code=None):
    super(Text, self).__init__(text)

    self.hint_language_code = hint_language_code

  def __str__(self):
    if len(self.raw) > 1000:
      return u"{}...{}".format(self.raw[:500], self.raw[-500:])
    else:
      return self.raw

class Breaker(object):
  """ Base class to segment text."""

  def __init__(self, locale):
    self.locale = Locale('locale')
    self.breaker = None

  def transform(self, sequence):
    seq = Sequence(sequence.text)
    seq.idx = [0]
    for segment in sequence:
      offset = seq.idx[-1]
      self.breaker.setText(segment)
      seq.idx.extend([offset+x for x in self.breaker])
    return seq

 
class SentenceTokenizer(Breaker):
  """ Segment text to sentences. """

  def __init__(self, locale='en'):
    super(SentenceTokenizer, self).__init__(locale)
    self.breaker = BreakIterator.createSentenceInstance(self.locale)


class WordTokenizer(Breaker):
  """ Segment text to words or tokens."""

  def __init__(self, locale='en'):
    super(WordTokenizer, self).__init__(locale)
    self.breaker = BreakIterator.createWordInstance(self.locale)


class Sequence(object):
  """ Text with indices indicates boundaries."""

  def __init__(self, text):

    if not text:
      raise ValueError("This Sequence is Empty")
    if not isinstance(text, unicode):
      raise ValueError("This is not unicode text instead {}".format(type(text)))

    self.__text = text
    self.idx = [0, len(self.text)]

  @property
  def text(self):
    return self.__text

  def __iter__(self):
    for start, end in zip(self.idx[:-1], self.idx[1:]):
      yield self.text[start: end]

  def tokens(self):
    """ Returns segmented text after stripping whitespace."""

    return [x.strip() for x in self if x.strip()]

  def __str__(self):
    if six.PY3:
      return self.__unicode__()
    return self.__unicode__().encode("utf-8")

  def __unicode__(self):
    return u'\n'.join(self.tokens())

  def split(self, sequence):
    """ Split into subsequences according to `sequence`."""

    major_idx = sequence.idx
    idx2 = 0
    for start, end in zip(major_idx[:-1], major_idx[1:]):
      idx1 = self.idx.index(start, idx2)
      idx2 = self.idx.index(end, idx2)
      seq = Sequence(self.text[start:end])
      seq.idx = [x-start for x in self.idx[idx1:idx2]]
      yield seq

  def __len__(self):
    return len(self.idx) - 1

  def empty(self):
    return not self.text.strip()
  
