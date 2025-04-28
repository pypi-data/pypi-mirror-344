(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_julia"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/julia.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/julia.js ***!
  \************************************************************************************************/
/***/ ((module) => {

/*
Language: Julia
Description: Julia is a high-level, high-performance, dynamic programming language.
Author: Kenta Sato <bicycle1885@gmail.com>
Contributors: Alex Arslan <ararslan@comcast.net>, Fredrik Ekre <ekrefredrik@gmail.com>
Website: https://julialang.org
*/

function julia(hljs) {
  // Since there are numerous special names in Julia, it is too much trouble
  // to maintain them by hand. Hence these names (i.e. keywords, literals and
  // built-ins) are automatically generated from Julia 1.5.2 itself through
  // the following scripts for each.

  // ref: https://docs.julialang.org/en/v1/manual/variables/#Allowed-Variable-Names
  var VARIABLE_NAME_RE = '[A-Za-z_\\u00A1-\\uFFFF][A-Za-z_0-9\\u00A1-\\uFFFF]*';

  // # keyword generator, multi-word keywords handled manually below (Julia 1.5.2)
  // import REPL.REPLCompletions
  // res = String["in", "isa", "where"]
  // for kw in collect(x.keyword for x in REPLCompletions.complete_keyword(""))
  //     if !(contains(kw, " ") || kw == "struct")
  //         push!(res, kw)
  //     end
  // end
  // sort!(unique!(res))
  // foreach(x -> println("\'", x, "\',"), res)
  var KEYWORD_LIST = [
    'baremodule',
    'begin',
    'break',
    'catch',
    'ccall',
    'const',
    'continue',
    'do',
    'else',
    'elseif',
    'end',
    'export',
    'false',
    'finally',
    'for',
    'function',
    'global',
    'if',
    'import',
    'in',
    'isa',
    'let',
    'local',
    'macro',
    'module',
    'quote',
    'return',
    'true',
    'try',
    'using',
    'where',
    'while',
  ];

  // # literal generator (Julia 1.5.2)
  // import REPL.REPLCompletions
  // res = String["true", "false"]
  // for compl in filter!(x -> isa(x, REPLCompletions.ModuleCompletion) && (x.parent === Base || x.parent === Core),
  //                     REPLCompletions.completions("", 0)[1])
  //     try
  //         v = eval(Symbol(compl.mod))
  //         if !(v isa Function || v isa Type || v isa TypeVar || v isa Module || v isa Colon)
  //             push!(res, compl.mod)
  //         end
  //     catch e
  //     end
  // end
  // sort!(unique!(res))
  // foreach(x -> println("\'", x, "\',"), res)
  var LITERAL_LIST = [
    'ARGS',
    'C_NULL',
    'DEPOT_PATH',
    'ENDIAN_BOM',
    'ENV',
    'Inf',
    'Inf16',
    'Inf32',
    'Inf64',
    'InsertionSort',
    'LOAD_PATH',
    'MergeSort',
    'NaN',
    'NaN16',
    'NaN32',
    'NaN64',
    'PROGRAM_FILE',
    'QuickSort',
    'RoundDown',
    'RoundFromZero',
    'RoundNearest',
    'RoundNearestTiesAway',
    'RoundNearestTiesUp',
    'RoundToZero',
    'RoundUp',
    'VERSION|0',
    'devnull',
    'false',
    'im',
    'missing',
    'nothing',
    'pi',
    'stderr',
    'stdin',
    'stdout',
    'true',
    'undef',
    'π',
    'ℯ',
  ];

  // # built_in generator (Julia 1.5.2)
  // import REPL.REPLCompletions
  // res = String[]
  // for compl in filter!(x -> isa(x, REPLCompletions.ModuleCompletion) && (x.parent === Base || x.parent === Core),
  //                     REPLCompletions.completions("", 0)[1])
  //     try
  //         v = eval(Symbol(compl.mod))
  //         if (v isa Type || v isa TypeVar) && (compl.mod != "=>")
  //             push!(res, compl.mod)
  //         end
  //     catch e
  //     end
  // end
  // sort!(unique!(res))
  // foreach(x -> println("\'", x, "\',"), res)
  var BUILT_IN_LIST = [
    'AbstractArray',
    'AbstractChannel',
    'AbstractChar',
    'AbstractDict',
    'AbstractDisplay',
    'AbstractFloat',
    'AbstractIrrational',
    'AbstractMatrix',
    'AbstractRange',
    'AbstractSet',
    'AbstractString',
    'AbstractUnitRange',
    'AbstractVecOrMat',
    'AbstractVector',
    'Any',
    'ArgumentError',
    'Array',
    'AssertionError',
    'BigFloat',
    'BigInt',
    'BitArray',
    'BitMatrix',
    'BitSet',
    'BitVector',
    'Bool',
    'BoundsError',
    'CapturedException',
    'CartesianIndex',
    'CartesianIndices',
    'Cchar',
    'Cdouble',
    'Cfloat',
    'Channel',
    'Char',
    'Cint',
    'Cintmax_t',
    'Clong',
    'Clonglong',
    'Cmd',
    'Colon',
    'Complex',
    'ComplexF16',
    'ComplexF32',
    'ComplexF64',
    'CompositeException',
    'Condition',
    'Cptrdiff_t',
    'Cshort',
    'Csize_t',
    'Cssize_t',
    'Cstring',
    'Cuchar',
    'Cuint',
    'Cuintmax_t',
    'Culong',
    'Culonglong',
    'Cushort',
    'Cvoid',
    'Cwchar_t',
    'Cwstring',
    'DataType',
    'DenseArray',
    'DenseMatrix',
    'DenseVecOrMat',
    'DenseVector',
    'Dict',
    'DimensionMismatch',
    'Dims',
    'DivideError',
    'DomainError',
    'EOFError',
    'Enum',
    'ErrorException',
    'Exception',
    'ExponentialBackOff',
    'Expr',
    'Float16',
    'Float32',
    'Float64',
    'Function',
    'GlobalRef',
    'HTML',
    'IO',
    'IOBuffer',
    'IOContext',
    'IOStream',
    'IdDict',
    'IndexCartesian',
    'IndexLinear',
    'IndexStyle',
    'InexactError',
    'InitError',
    'Int',
    'Int128',
    'Int16',
    'Int32',
    'Int64',
    'Int8',
    'Integer',
    'InterruptException',
    'InvalidStateException',
    'Irrational',
    'KeyError',
    'LinRange',
    'LineNumberNode',
    'LinearIndices',
    'LoadError',
    'MIME',
    'Matrix',
    'Method',
    'MethodError',
    'Missing',
    'MissingException',
    'Module',
    'NTuple',
    'NamedTuple',
    'Nothing',
    'Number',
    'OrdinalRange',
    'OutOfMemoryError',
    'OverflowError',
    'Pair',
    'PartialQuickSort',
    'PermutedDimsArray',
    'Pipe',
    'ProcessFailedException',
    'Ptr',
    'QuoteNode',
    'Rational',
    'RawFD',
    'ReadOnlyMemoryError',
    'Real',
    'ReentrantLock',
    'Ref',
    'Regex',
    'RegexMatch',
    'RoundingMode',
    'SegmentationFault',
    'Set',
    'Signed',
    'Some',
    'StackOverflowError',
    'StepRange',
    'StepRangeLen',
    'StridedArray',
    'StridedMatrix',
    'StridedVecOrMat',
    'StridedVector',
    'String',
    'StringIndexError',
    'SubArray',
    'SubString',
    'SubstitutionString',
    'Symbol',
    'SystemError',
    'Task',
    'TaskFailedException',
    'Text',
    'TextDisplay',
    'Timer',
    'Tuple',
    'Type',
    'TypeError',
    'TypeVar',
    'UInt',
    'UInt128',
    'UInt16',
    'UInt32',
    'UInt64',
    'UInt8',
    'UndefInitializer',
    'UndefKeywordError',
    'UndefRefError',
    'UndefVarError',
    'Union',
    'UnionAll',
    'UnitRange',
    'Unsigned',
    'Val',
    'Vararg',
    'VecElement',
    'VecOrMat',
    'Vector',
    'VersionNumber',
    'WeakKeyDict',
    'WeakRef',
  ];

  var KEYWORDS = {
    $pattern: VARIABLE_NAME_RE,
    keyword: KEYWORD_LIST,
    literal: LITERAL_LIST,
    built_in: BUILT_IN_LIST,
  };

  // placeholder for recursive self-reference
  var DEFAULT = {
    keywords: KEYWORDS, illegal: /<\//
  };

  // ref: https://docs.julialang.org/en/v1/manual/integers-and-floating-point-numbers/
  var NUMBER = {
    className: 'number',
    // supported numeric literals:
    //  * binary literal (e.g. 0x10)
    //  * octal literal (e.g. 0o76543210)
    //  * hexadecimal literal (e.g. 0xfedcba876543210)
    //  * hexadecimal floating point literal (e.g. 0x1p0, 0x1.2p2)
    //  * decimal literal (e.g. 9876543210, 100_000_000)
    //  * floating pointe literal (e.g. 1.2, 1.2f, .2, 1., 1.2e10, 1.2e-10)
    begin: /(\b0x[\d_]*(\.[\d_]*)?|0x\.\d[\d_]*)p[-+]?\d+|\b0[box][a-fA-F0-9][a-fA-F0-9_]*|(\b\d[\d_]*(\.[\d_]*)?|\.\d[\d_]*)([eEfF][-+]?\d+)?/,
    relevance: 0
  };

  var CHAR = {
    className: 'string',
    begin: /'(.|\\[xXuU][a-zA-Z0-9]+)'/
  };

  var INTERPOLATION = {
    className: 'subst',
    begin: /\$\(/, end: /\)/,
    keywords: KEYWORDS
  };

  var INTERPOLATED_VARIABLE = {
    className: 'variable',
    begin: '\\$' + VARIABLE_NAME_RE
  };

  // TODO: neatly escape normal code in string literal
  var STRING = {
    className: 'string',
    contains: [hljs.BACKSLASH_ESCAPE, INTERPOLATION, INTERPOLATED_VARIABLE],
    variants: [
      { begin: /\w*"""/, end: /"""\w*/, relevance: 10 },
      { begin: /\w*"/, end: /"\w*/ }
    ]
  };

  var COMMAND = {
    className: 'string',
    contains: [hljs.BACKSLASH_ESCAPE, INTERPOLATION, INTERPOLATED_VARIABLE],
    begin: '`', end: '`'
  };

  var MACROCALL = {
    className: 'meta',
    begin: '@' + VARIABLE_NAME_RE
  };

  var COMMENT = {
    className: 'comment',
    variants: [
      { begin: '#=', end: '=#', relevance: 10 },
      { begin: '#', end: '$' }
    ]
  };

  DEFAULT.name = 'Julia';
  DEFAULT.contains = [
    NUMBER,
    CHAR,
    STRING,
    COMMAND,
    MACROCALL,
    COMMENT,
    hljs.HASH_COMMENT_MODE,
    {
      className: 'keyword',
      begin:
        '\\b(((abstract|primitive)\\s+)type|(mutable\\s+)?struct)\\b'
    },
    {begin: /<:/}  // relevance booster
  ];
  INTERPOLATION.contains = DEFAULT.contains;

  return DEFAULT;
}

module.exports = julia;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfanVsaWEuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxRQUFRLCtDQUErQztBQUN2RCxRQUFRO0FBQ1I7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLFFBQVEsdUNBQXVDO0FBQy9DLFFBQVE7QUFDUjtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMLEtBQUssY0FBYztBQUNuQjtBQUNBOztBQUVBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2p1bGlhLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogSnVsaWFcbkRlc2NyaXB0aW9uOiBKdWxpYSBpcyBhIGhpZ2gtbGV2ZWwsIGhpZ2gtcGVyZm9ybWFuY2UsIGR5bmFtaWMgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2UuXG5BdXRob3I6IEtlbnRhIFNhdG8gPGJpY3ljbGUxODg1QGdtYWlsLmNvbT5cbkNvbnRyaWJ1dG9yczogQWxleCBBcnNsYW4gPGFyYXJzbGFuQGNvbWNhc3QubmV0PiwgRnJlZHJpayBFa3JlIDxla3JlZnJlZHJpa0BnbWFpbC5jb20+XG5XZWJzaXRlOiBodHRwczovL2p1bGlhbGFuZy5vcmdcbiovXG5cbmZ1bmN0aW9uIGp1bGlhKGhsanMpIHtcbiAgLy8gU2luY2UgdGhlcmUgYXJlIG51bWVyb3VzIHNwZWNpYWwgbmFtZXMgaW4gSnVsaWEsIGl0IGlzIHRvbyBtdWNoIHRyb3VibGVcbiAgLy8gdG8gbWFpbnRhaW4gdGhlbSBieSBoYW5kLiBIZW5jZSB0aGVzZSBuYW1lcyAoaS5lLiBrZXl3b3JkcywgbGl0ZXJhbHMgYW5kXG4gIC8vIGJ1aWx0LWlucykgYXJlIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGZyb20gSnVsaWEgMS41LjIgaXRzZWxmIHRocm91Z2hcbiAgLy8gdGhlIGZvbGxvd2luZyBzY3JpcHRzIGZvciBlYWNoLlxuXG4gIC8vIHJlZjogaHR0cHM6Ly9kb2NzLmp1bGlhbGFuZy5vcmcvZW4vdjEvbWFudWFsL3ZhcmlhYmxlcy8jQWxsb3dlZC1WYXJpYWJsZS1OYW1lc1xuICB2YXIgVkFSSUFCTEVfTkFNRV9SRSA9ICdbQS1aYS16X1xcXFx1MDBBMS1cXFxcdUZGRkZdW0EtWmEtel8wLTlcXFxcdTAwQTEtXFxcXHVGRkZGXSonO1xuXG4gIC8vICMga2V5d29yZCBnZW5lcmF0b3IsIG11bHRpLXdvcmQga2V5d29yZHMgaGFuZGxlZCBtYW51YWxseSBiZWxvdyAoSnVsaWEgMS41LjIpXG4gIC8vIGltcG9ydCBSRVBMLlJFUExDb21wbGV0aW9uc1xuICAvLyByZXMgPSBTdHJpbmdbXCJpblwiLCBcImlzYVwiLCBcIndoZXJlXCJdXG4gIC8vIGZvciBrdyBpbiBjb2xsZWN0KHgua2V5d29yZCBmb3IgeCBpbiBSRVBMQ29tcGxldGlvbnMuY29tcGxldGVfa2V5d29yZChcIlwiKSlcbiAgLy8gICAgIGlmICEoY29udGFpbnMoa3csIFwiIFwiKSB8fCBrdyA9PSBcInN0cnVjdFwiKVxuICAvLyAgICAgICAgIHB1c2ghKHJlcywga3cpXG4gIC8vICAgICBlbmRcbiAgLy8gZW5kXG4gIC8vIHNvcnQhKHVuaXF1ZSEocmVzKSlcbiAgLy8gZm9yZWFjaCh4IC0+IHByaW50bG4oXCJcXCdcIiwgeCwgXCJcXCcsXCIpLCByZXMpXG4gIHZhciBLRVlXT1JEX0xJU1QgPSBbXG4gICAgJ2JhcmVtb2R1bGUnLFxuICAgICdiZWdpbicsXG4gICAgJ2JyZWFrJyxcbiAgICAnY2F0Y2gnLFxuICAgICdjY2FsbCcsXG4gICAgJ2NvbnN0JyxcbiAgICAnY29udGludWUnLFxuICAgICdkbycsXG4gICAgJ2Vsc2UnLFxuICAgICdlbHNlaWYnLFxuICAgICdlbmQnLFxuICAgICdleHBvcnQnLFxuICAgICdmYWxzZScsXG4gICAgJ2ZpbmFsbHknLFxuICAgICdmb3InLFxuICAgICdmdW5jdGlvbicsXG4gICAgJ2dsb2JhbCcsXG4gICAgJ2lmJyxcbiAgICAnaW1wb3J0JyxcbiAgICAnaW4nLFxuICAgICdpc2EnLFxuICAgICdsZXQnLFxuICAgICdsb2NhbCcsXG4gICAgJ21hY3JvJyxcbiAgICAnbW9kdWxlJyxcbiAgICAncXVvdGUnLFxuICAgICdyZXR1cm4nLFxuICAgICd0cnVlJyxcbiAgICAndHJ5JyxcbiAgICAndXNpbmcnLFxuICAgICd3aGVyZScsXG4gICAgJ3doaWxlJyxcbiAgXTtcblxuICAvLyAjIGxpdGVyYWwgZ2VuZXJhdG9yIChKdWxpYSAxLjUuMilcbiAgLy8gaW1wb3J0IFJFUEwuUkVQTENvbXBsZXRpb25zXG4gIC8vIHJlcyA9IFN0cmluZ1tcInRydWVcIiwgXCJmYWxzZVwiXVxuICAvLyBmb3IgY29tcGwgaW4gZmlsdGVyISh4IC0+IGlzYSh4LCBSRVBMQ29tcGxldGlvbnMuTW9kdWxlQ29tcGxldGlvbikgJiYgKHgucGFyZW50ID09PSBCYXNlIHx8IHgucGFyZW50ID09PSBDb3JlKSxcbiAgLy8gICAgICAgICAgICAgICAgICAgICBSRVBMQ29tcGxldGlvbnMuY29tcGxldGlvbnMoXCJcIiwgMClbMV0pXG4gIC8vICAgICB0cnlcbiAgLy8gICAgICAgICB2ID0gZXZhbChTeW1ib2woY29tcGwubW9kKSlcbiAgLy8gICAgICAgICBpZiAhKHYgaXNhIEZ1bmN0aW9uIHx8IHYgaXNhIFR5cGUgfHwgdiBpc2EgVHlwZVZhciB8fCB2IGlzYSBNb2R1bGUgfHwgdiBpc2EgQ29sb24pXG4gIC8vICAgICAgICAgICAgIHB1c2ghKHJlcywgY29tcGwubW9kKVxuICAvLyAgICAgICAgIGVuZFxuICAvLyAgICAgY2F0Y2ggZVxuICAvLyAgICAgZW5kXG4gIC8vIGVuZFxuICAvLyBzb3J0ISh1bmlxdWUhKHJlcykpXG4gIC8vIGZvcmVhY2goeCAtPiBwcmludGxuKFwiXFwnXCIsIHgsIFwiXFwnLFwiKSwgcmVzKVxuICB2YXIgTElURVJBTF9MSVNUID0gW1xuICAgICdBUkdTJyxcbiAgICAnQ19OVUxMJyxcbiAgICAnREVQT1RfUEFUSCcsXG4gICAgJ0VORElBTl9CT00nLFxuICAgICdFTlYnLFxuICAgICdJbmYnLFxuICAgICdJbmYxNicsXG4gICAgJ0luZjMyJyxcbiAgICAnSW5mNjQnLFxuICAgICdJbnNlcnRpb25Tb3J0JyxcbiAgICAnTE9BRF9QQVRIJyxcbiAgICAnTWVyZ2VTb3J0JyxcbiAgICAnTmFOJyxcbiAgICAnTmFOMTYnLFxuICAgICdOYU4zMicsXG4gICAgJ05hTjY0JyxcbiAgICAnUFJPR1JBTV9GSUxFJyxcbiAgICAnUXVpY2tTb3J0JyxcbiAgICAnUm91bmREb3duJyxcbiAgICAnUm91bmRGcm9tWmVybycsXG4gICAgJ1JvdW5kTmVhcmVzdCcsXG4gICAgJ1JvdW5kTmVhcmVzdFRpZXNBd2F5JyxcbiAgICAnUm91bmROZWFyZXN0VGllc1VwJyxcbiAgICAnUm91bmRUb1plcm8nLFxuICAgICdSb3VuZFVwJyxcbiAgICAnVkVSU0lPTnwwJyxcbiAgICAnZGV2bnVsbCcsXG4gICAgJ2ZhbHNlJyxcbiAgICAnaW0nLFxuICAgICdtaXNzaW5nJyxcbiAgICAnbm90aGluZycsXG4gICAgJ3BpJyxcbiAgICAnc3RkZXJyJyxcbiAgICAnc3RkaW4nLFxuICAgICdzdGRvdXQnLFxuICAgICd0cnVlJyxcbiAgICAndW5kZWYnLFxuICAgICfPgCcsXG4gICAgJ+KErycsXG4gIF07XG5cbiAgLy8gIyBidWlsdF9pbiBnZW5lcmF0b3IgKEp1bGlhIDEuNS4yKVxuICAvLyBpbXBvcnQgUkVQTC5SRVBMQ29tcGxldGlvbnNcbiAgLy8gcmVzID0gU3RyaW5nW11cbiAgLy8gZm9yIGNvbXBsIGluIGZpbHRlciEoeCAtPiBpc2EoeCwgUkVQTENvbXBsZXRpb25zLk1vZHVsZUNvbXBsZXRpb24pICYmICh4LnBhcmVudCA9PT0gQmFzZSB8fCB4LnBhcmVudCA9PT0gQ29yZSksXG4gIC8vICAgICAgICAgICAgICAgICAgICAgUkVQTENvbXBsZXRpb25zLmNvbXBsZXRpb25zKFwiXCIsIDApWzFdKVxuICAvLyAgICAgdHJ5XG4gIC8vICAgICAgICAgdiA9IGV2YWwoU3ltYm9sKGNvbXBsLm1vZCkpXG4gIC8vICAgICAgICAgaWYgKHYgaXNhIFR5cGUgfHwgdiBpc2EgVHlwZVZhcikgJiYgKGNvbXBsLm1vZCAhPSBcIj0+XCIpXG4gIC8vICAgICAgICAgICAgIHB1c2ghKHJlcywgY29tcGwubW9kKVxuICAvLyAgICAgICAgIGVuZFxuICAvLyAgICAgY2F0Y2ggZVxuICAvLyAgICAgZW5kXG4gIC8vIGVuZFxuICAvLyBzb3J0ISh1bmlxdWUhKHJlcykpXG4gIC8vIGZvcmVhY2goeCAtPiBwcmludGxuKFwiXFwnXCIsIHgsIFwiXFwnLFwiKSwgcmVzKVxuICB2YXIgQlVJTFRfSU5fTElTVCA9IFtcbiAgICAnQWJzdHJhY3RBcnJheScsXG4gICAgJ0Fic3RyYWN0Q2hhbm5lbCcsXG4gICAgJ0Fic3RyYWN0Q2hhcicsXG4gICAgJ0Fic3RyYWN0RGljdCcsXG4gICAgJ0Fic3RyYWN0RGlzcGxheScsXG4gICAgJ0Fic3RyYWN0RmxvYXQnLFxuICAgICdBYnN0cmFjdElycmF0aW9uYWwnLFxuICAgICdBYnN0cmFjdE1hdHJpeCcsXG4gICAgJ0Fic3RyYWN0UmFuZ2UnLFxuICAgICdBYnN0cmFjdFNldCcsXG4gICAgJ0Fic3RyYWN0U3RyaW5nJyxcbiAgICAnQWJzdHJhY3RVbml0UmFuZ2UnLFxuICAgICdBYnN0cmFjdFZlY09yTWF0JyxcbiAgICAnQWJzdHJhY3RWZWN0b3InLFxuICAgICdBbnknLFxuICAgICdBcmd1bWVudEVycm9yJyxcbiAgICAnQXJyYXknLFxuICAgICdBc3NlcnRpb25FcnJvcicsXG4gICAgJ0JpZ0Zsb2F0JyxcbiAgICAnQmlnSW50JyxcbiAgICAnQml0QXJyYXknLFxuICAgICdCaXRNYXRyaXgnLFxuICAgICdCaXRTZXQnLFxuICAgICdCaXRWZWN0b3InLFxuICAgICdCb29sJyxcbiAgICAnQm91bmRzRXJyb3InLFxuICAgICdDYXB0dXJlZEV4Y2VwdGlvbicsXG4gICAgJ0NhcnRlc2lhbkluZGV4JyxcbiAgICAnQ2FydGVzaWFuSW5kaWNlcycsXG4gICAgJ0NjaGFyJyxcbiAgICAnQ2RvdWJsZScsXG4gICAgJ0NmbG9hdCcsXG4gICAgJ0NoYW5uZWwnLFxuICAgICdDaGFyJyxcbiAgICAnQ2ludCcsXG4gICAgJ0NpbnRtYXhfdCcsXG4gICAgJ0Nsb25nJyxcbiAgICAnQ2xvbmdsb25nJyxcbiAgICAnQ21kJyxcbiAgICAnQ29sb24nLFxuICAgICdDb21wbGV4JyxcbiAgICAnQ29tcGxleEYxNicsXG4gICAgJ0NvbXBsZXhGMzInLFxuICAgICdDb21wbGV4RjY0JyxcbiAgICAnQ29tcG9zaXRlRXhjZXB0aW9uJyxcbiAgICAnQ29uZGl0aW9uJyxcbiAgICAnQ3B0cmRpZmZfdCcsXG4gICAgJ0NzaG9ydCcsXG4gICAgJ0NzaXplX3QnLFxuICAgICdDc3NpemVfdCcsXG4gICAgJ0NzdHJpbmcnLFxuICAgICdDdWNoYXInLFxuICAgICdDdWludCcsXG4gICAgJ0N1aW50bWF4X3QnLFxuICAgICdDdWxvbmcnLFxuICAgICdDdWxvbmdsb25nJyxcbiAgICAnQ3VzaG9ydCcsXG4gICAgJ0N2b2lkJyxcbiAgICAnQ3djaGFyX3QnLFxuICAgICdDd3N0cmluZycsXG4gICAgJ0RhdGFUeXBlJyxcbiAgICAnRGVuc2VBcnJheScsXG4gICAgJ0RlbnNlTWF0cml4JyxcbiAgICAnRGVuc2VWZWNPck1hdCcsXG4gICAgJ0RlbnNlVmVjdG9yJyxcbiAgICAnRGljdCcsXG4gICAgJ0RpbWVuc2lvbk1pc21hdGNoJyxcbiAgICAnRGltcycsXG4gICAgJ0RpdmlkZUVycm9yJyxcbiAgICAnRG9tYWluRXJyb3InLFxuICAgICdFT0ZFcnJvcicsXG4gICAgJ0VudW0nLFxuICAgICdFcnJvckV4Y2VwdGlvbicsXG4gICAgJ0V4Y2VwdGlvbicsXG4gICAgJ0V4cG9uZW50aWFsQmFja09mZicsXG4gICAgJ0V4cHInLFxuICAgICdGbG9hdDE2JyxcbiAgICAnRmxvYXQzMicsXG4gICAgJ0Zsb2F0NjQnLFxuICAgICdGdW5jdGlvbicsXG4gICAgJ0dsb2JhbFJlZicsXG4gICAgJ0hUTUwnLFxuICAgICdJTycsXG4gICAgJ0lPQnVmZmVyJyxcbiAgICAnSU9Db250ZXh0JyxcbiAgICAnSU9TdHJlYW0nLFxuICAgICdJZERpY3QnLFxuICAgICdJbmRleENhcnRlc2lhbicsXG4gICAgJ0luZGV4TGluZWFyJyxcbiAgICAnSW5kZXhTdHlsZScsXG4gICAgJ0luZXhhY3RFcnJvcicsXG4gICAgJ0luaXRFcnJvcicsXG4gICAgJ0ludCcsXG4gICAgJ0ludDEyOCcsXG4gICAgJ0ludDE2JyxcbiAgICAnSW50MzInLFxuICAgICdJbnQ2NCcsXG4gICAgJ0ludDgnLFxuICAgICdJbnRlZ2VyJyxcbiAgICAnSW50ZXJydXB0RXhjZXB0aW9uJyxcbiAgICAnSW52YWxpZFN0YXRlRXhjZXB0aW9uJyxcbiAgICAnSXJyYXRpb25hbCcsXG4gICAgJ0tleUVycm9yJyxcbiAgICAnTGluUmFuZ2UnLFxuICAgICdMaW5lTnVtYmVyTm9kZScsXG4gICAgJ0xpbmVhckluZGljZXMnLFxuICAgICdMb2FkRXJyb3InLFxuICAgICdNSU1FJyxcbiAgICAnTWF0cml4JyxcbiAgICAnTWV0aG9kJyxcbiAgICAnTWV0aG9kRXJyb3InLFxuICAgICdNaXNzaW5nJyxcbiAgICAnTWlzc2luZ0V4Y2VwdGlvbicsXG4gICAgJ01vZHVsZScsXG4gICAgJ05UdXBsZScsXG4gICAgJ05hbWVkVHVwbGUnLFxuICAgICdOb3RoaW5nJyxcbiAgICAnTnVtYmVyJyxcbiAgICAnT3JkaW5hbFJhbmdlJyxcbiAgICAnT3V0T2ZNZW1vcnlFcnJvcicsXG4gICAgJ092ZXJmbG93RXJyb3InLFxuICAgICdQYWlyJyxcbiAgICAnUGFydGlhbFF1aWNrU29ydCcsXG4gICAgJ1Blcm11dGVkRGltc0FycmF5JyxcbiAgICAnUGlwZScsXG4gICAgJ1Byb2Nlc3NGYWlsZWRFeGNlcHRpb24nLFxuICAgICdQdHInLFxuICAgICdRdW90ZU5vZGUnLFxuICAgICdSYXRpb25hbCcsXG4gICAgJ1Jhd0ZEJyxcbiAgICAnUmVhZE9ubHlNZW1vcnlFcnJvcicsXG4gICAgJ1JlYWwnLFxuICAgICdSZWVudHJhbnRMb2NrJyxcbiAgICAnUmVmJyxcbiAgICAnUmVnZXgnLFxuICAgICdSZWdleE1hdGNoJyxcbiAgICAnUm91bmRpbmdNb2RlJyxcbiAgICAnU2VnbWVudGF0aW9uRmF1bHQnLFxuICAgICdTZXQnLFxuICAgICdTaWduZWQnLFxuICAgICdTb21lJyxcbiAgICAnU3RhY2tPdmVyZmxvd0Vycm9yJyxcbiAgICAnU3RlcFJhbmdlJyxcbiAgICAnU3RlcFJhbmdlTGVuJyxcbiAgICAnU3RyaWRlZEFycmF5JyxcbiAgICAnU3RyaWRlZE1hdHJpeCcsXG4gICAgJ1N0cmlkZWRWZWNPck1hdCcsXG4gICAgJ1N0cmlkZWRWZWN0b3InLFxuICAgICdTdHJpbmcnLFxuICAgICdTdHJpbmdJbmRleEVycm9yJyxcbiAgICAnU3ViQXJyYXknLFxuICAgICdTdWJTdHJpbmcnLFxuICAgICdTdWJzdGl0dXRpb25TdHJpbmcnLFxuICAgICdTeW1ib2wnLFxuICAgICdTeXN0ZW1FcnJvcicsXG4gICAgJ1Rhc2snLFxuICAgICdUYXNrRmFpbGVkRXhjZXB0aW9uJyxcbiAgICAnVGV4dCcsXG4gICAgJ1RleHREaXNwbGF5JyxcbiAgICAnVGltZXInLFxuICAgICdUdXBsZScsXG4gICAgJ1R5cGUnLFxuICAgICdUeXBlRXJyb3InLFxuICAgICdUeXBlVmFyJyxcbiAgICAnVUludCcsXG4gICAgJ1VJbnQxMjgnLFxuICAgICdVSW50MTYnLFxuICAgICdVSW50MzInLFxuICAgICdVSW50NjQnLFxuICAgICdVSW50OCcsXG4gICAgJ1VuZGVmSW5pdGlhbGl6ZXInLFxuICAgICdVbmRlZktleXdvcmRFcnJvcicsXG4gICAgJ1VuZGVmUmVmRXJyb3InLFxuICAgICdVbmRlZlZhckVycm9yJyxcbiAgICAnVW5pb24nLFxuICAgICdVbmlvbkFsbCcsXG4gICAgJ1VuaXRSYW5nZScsXG4gICAgJ1Vuc2lnbmVkJyxcbiAgICAnVmFsJyxcbiAgICAnVmFyYXJnJyxcbiAgICAnVmVjRWxlbWVudCcsXG4gICAgJ1ZlY09yTWF0JyxcbiAgICAnVmVjdG9yJyxcbiAgICAnVmVyc2lvbk51bWJlcicsXG4gICAgJ1dlYWtLZXlEaWN0JyxcbiAgICAnV2Vha1JlZicsXG4gIF07XG5cbiAgdmFyIEtFWVdPUkRTID0ge1xuICAgICRwYXR0ZXJuOiBWQVJJQUJMRV9OQU1FX1JFLFxuICAgIGtleXdvcmQ6IEtFWVdPUkRfTElTVCxcbiAgICBsaXRlcmFsOiBMSVRFUkFMX0xJU1QsXG4gICAgYnVpbHRfaW46IEJVSUxUX0lOX0xJU1QsXG4gIH07XG5cbiAgLy8gcGxhY2Vob2xkZXIgZm9yIHJlY3Vyc2l2ZSBzZWxmLXJlZmVyZW5jZVxuICB2YXIgREVGQVVMVCA9IHtcbiAgICBrZXl3b3JkczogS0VZV09SRFMsIGlsbGVnYWw6IC88XFwvL1xuICB9O1xuXG4gIC8vIHJlZjogaHR0cHM6Ly9kb2NzLmp1bGlhbGFuZy5vcmcvZW4vdjEvbWFudWFsL2ludGVnZXJzLWFuZC1mbG9hdGluZy1wb2ludC1udW1iZXJzL1xuICB2YXIgTlVNQkVSID0ge1xuICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgLy8gc3VwcG9ydGVkIG51bWVyaWMgbGl0ZXJhbHM6XG4gICAgLy8gICogYmluYXJ5IGxpdGVyYWwgKGUuZy4gMHgxMClcbiAgICAvLyAgKiBvY3RhbCBsaXRlcmFsIChlLmcuIDBvNzY1NDMyMTApXG4gICAgLy8gICogaGV4YWRlY2ltYWwgbGl0ZXJhbCAoZS5nLiAweGZlZGNiYTg3NjU0MzIxMClcbiAgICAvLyAgKiBoZXhhZGVjaW1hbCBmbG9hdGluZyBwb2ludCBsaXRlcmFsIChlLmcuIDB4MXAwLCAweDEuMnAyKVxuICAgIC8vICAqIGRlY2ltYWwgbGl0ZXJhbCAoZS5nLiA5ODc2NTQzMjEwLCAxMDBfMDAwXzAwMClcbiAgICAvLyAgKiBmbG9hdGluZyBwb2ludGUgbGl0ZXJhbCAoZS5nLiAxLjIsIDEuMmYsIC4yLCAxLiwgMS4yZTEwLCAxLjJlLTEwKVxuICAgIGJlZ2luOiAvKFxcYjB4W1xcZF9dKihcXC5bXFxkX10qKT98MHhcXC5cXGRbXFxkX10qKXBbLStdP1xcZCt8XFxiMFtib3hdW2EtZkEtRjAtOV1bYS1mQS1GMC05X10qfChcXGJcXGRbXFxkX10qKFxcLltcXGRfXSopP3xcXC5cXGRbXFxkX10qKShbZUVmRl1bLStdP1xcZCspPy8sXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgdmFyIENIQVIgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogLycoLnxcXFxcW3hYdVVdW2EtekEtWjAtOV0rKScvXG4gIH07XG5cbiAgdmFyIElOVEVSUE9MQVRJT04gPSB7XG4gICAgY2xhc3NOYW1lOiAnc3Vic3QnLFxuICAgIGJlZ2luOiAvXFwkXFwoLywgZW5kOiAvXFwpLyxcbiAgICBrZXl3b3JkczogS0VZV09SRFNcbiAgfTtcblxuICB2YXIgSU5URVJQT0xBVEVEX1ZBUklBQkxFID0ge1xuICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICBiZWdpbjogJ1xcXFwkJyArIFZBUklBQkxFX05BTUVfUkVcbiAgfTtcblxuICAvLyBUT0RPOiBuZWF0bHkgZXNjYXBlIG5vcm1hbCBjb2RlIGluIHN0cmluZyBsaXRlcmFsXG4gIHZhciBTVFJJTkcgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBjb250YWluczogW2hsanMuQkFDS1NMQVNIX0VTQ0FQRSwgSU5URVJQT0xBVElPTiwgSU5URVJQT0xBVEVEX1ZBUklBQkxFXSxcbiAgICB2YXJpYW50czogW1xuICAgICAgeyBiZWdpbjogL1xcdypcIlwiXCIvLCBlbmQ6IC9cIlwiXCJcXHcqLywgcmVsZXZhbmNlOiAxMCB9LFxuICAgICAgeyBiZWdpbjogL1xcdypcIi8sIGVuZDogL1wiXFx3Ki8gfVxuICAgIF1cbiAgfTtcblxuICB2YXIgQ09NTUFORCA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGNvbnRhaW5zOiBbaGxqcy5CQUNLU0xBU0hfRVNDQVBFLCBJTlRFUlBPTEFUSU9OLCBJTlRFUlBPTEFURURfVkFSSUFCTEVdLFxuICAgIGJlZ2luOiAnYCcsIGVuZDogJ2AnXG4gIH07XG5cbiAgdmFyIE1BQ1JPQ0FMTCA9IHtcbiAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICBiZWdpbjogJ0AnICsgVkFSSUFCTEVfTkFNRV9SRVxuICB9O1xuXG4gIHZhciBDT01NRU5UID0ge1xuICAgIGNsYXNzTmFtZTogJ2NvbW1lbnQnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7IGJlZ2luOiAnIz0nLCBlbmQ6ICc9IycsIHJlbGV2YW5jZTogMTAgfSxcbiAgICAgIHsgYmVnaW46ICcjJywgZW5kOiAnJCcgfVxuICAgIF1cbiAgfTtcblxuICBERUZBVUxULm5hbWUgPSAnSnVsaWEnO1xuICBERUZBVUxULmNvbnRhaW5zID0gW1xuICAgIE5VTUJFUixcbiAgICBDSEFSLFxuICAgIFNUUklORyxcbiAgICBDT01NQU5ELFxuICAgIE1BQ1JPQ0FMTCxcbiAgICBDT01NRU5ULFxuICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgICBiZWdpbjpcbiAgICAgICAgJ1xcXFxiKCgoYWJzdHJhY3R8cHJpbWl0aXZlKVxcXFxzKyl0eXBlfChtdXRhYmxlXFxcXHMrKT9zdHJ1Y3QpXFxcXGInXG4gICAgfSxcbiAgICB7YmVnaW46IC88Oi99ICAvLyByZWxldmFuY2UgYm9vc3RlclxuICBdO1xuICBJTlRFUlBPTEFUSU9OLmNvbnRhaW5zID0gREVGQVVMVC5jb250YWlucztcblxuICByZXR1cm4gREVGQVVMVDtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBqdWxpYTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==