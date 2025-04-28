(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_sql"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/sql.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/sql.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/**
 * @param {string} value
 * @returns {RegExp}
 * */

/**
 * @param {RegExp | string } re
 * @returns {string}
 */
function source(re) {
  if (!re) return null;
  if (typeof re === "string") return re;

  return re.source;
}

/**
 * @param {...(RegExp | string) } args
 * @returns {string}
 */
function concat(...args) {
  const joined = args.map((x) => source(x)).join("");
  return joined;
}

/**
 * Any of the passed expresssions may match
 *
 * Creates a huge this | this | that | that match
 * @param {(RegExp | string)[] } args
 * @returns {string}
 */
function either(...args) {
  const joined = '(' + args.map((x) => source(x)).join("|") + ")";
  return joined;
}

/*
 Language: SQL
 Website: https://en.wikipedia.org/wiki/SQL
 Category: common, database
 */

function sql(hljs) {
  const COMMENT_MODE = hljs.COMMENT('--', '$');
  const STRING = {
    className: 'string',
    variants: [
      {
        begin: /'/,
        end: /'/,
        contains: [
          {begin: /''/ }
        ]
      }
    ]
  };
  const QUOTED_IDENTIFIER = {
    begin: /"/,
    end: /"/,
    contains: [ { begin: /""/ } ]
  };

  const LITERALS = [
    "true",
    "false",
    // Not sure it's correct to call NULL literal, and clauses like IS [NOT] NULL look strange that way.
    // "null",
    "unknown"
  ];

  const MULTI_WORD_TYPES = [
    "double precision",
    "large object",
    "with timezone",
    "without timezone"
  ];

  const TYPES = [
    'bigint',
    'binary',
    'blob',
    'boolean',
    'char',
    'character',
    'clob',
    'date',
    'dec',
    'decfloat',
    'decimal',
    'float',
    'int',
    'integer',
    'interval',
    'nchar',
    'nclob',
    'national',
    'numeric',
    'real',
    'row',
    'smallint',
    'time',
    'timestamp',
    'varchar',
    'varying', // modifier (character varying)
    'varbinary'
  ];

  const NON_RESERVED_WORDS = [
    "add",
    "asc",
    "collation",
    "desc",
    "final",
    "first",
    "last",
    "view"
  ];

  // https://jakewheat.github.io/sql-overview/sql-2016-foundation-grammar.html#reserved-word
  const RESERVED_WORDS = [
    "abs",
    "acos",
    "all",
    "allocate",
    "alter",
    "and",
    "any",
    "are",
    "array",
    "array_agg",
    "array_max_cardinality",
    "as",
    "asensitive",
    "asin",
    "asymmetric",
    "at",
    "atan",
    "atomic",
    "authorization",
    "avg",
    "begin",
    "begin_frame",
    "begin_partition",
    "between",
    "bigint",
    "binary",
    "blob",
    "boolean",
    "both",
    "by",
    "call",
    "called",
    "cardinality",
    "cascaded",
    "case",
    "cast",
    "ceil",
    "ceiling",
    "char",
    "char_length",
    "character",
    "character_length",
    "check",
    "classifier",
    "clob",
    "close",
    "coalesce",
    "collate",
    "collect",
    "column",
    "commit",
    "condition",
    "connect",
    "constraint",
    "contains",
    "convert",
    "copy",
    "corr",
    "corresponding",
    "cos",
    "cosh",
    "count",
    "covar_pop",
    "covar_samp",
    "create",
    "cross",
    "cube",
    "cume_dist",
    "current",
    "current_catalog",
    "current_date",
    "current_default_transform_group",
    "current_path",
    "current_role",
    "current_row",
    "current_schema",
    "current_time",
    "current_timestamp",
    "current_path",
    "current_role",
    "current_transform_group_for_type",
    "current_user",
    "cursor",
    "cycle",
    "date",
    "day",
    "deallocate",
    "dec",
    "decimal",
    "decfloat",
    "declare",
    "default",
    "define",
    "delete",
    "dense_rank",
    "deref",
    "describe",
    "deterministic",
    "disconnect",
    "distinct",
    "double",
    "drop",
    "dynamic",
    "each",
    "element",
    "else",
    "empty",
    "end",
    "end_frame",
    "end_partition",
    "end-exec",
    "equals",
    "escape",
    "every",
    "except",
    "exec",
    "execute",
    "exists",
    "exp",
    "external",
    "extract",
    "false",
    "fetch",
    "filter",
    "first_value",
    "float",
    "floor",
    "for",
    "foreign",
    "frame_row",
    "free",
    "from",
    "full",
    "function",
    "fusion",
    "get",
    "global",
    "grant",
    "group",
    "grouping",
    "groups",
    "having",
    "hold",
    "hour",
    "identity",
    "in",
    "indicator",
    "initial",
    "inner",
    "inout",
    "insensitive",
    "insert",
    "int",
    "integer",
    "intersect",
    "intersection",
    "interval",
    "into",
    "is",
    "join",
    "json_array",
    "json_arrayagg",
    "json_exists",
    "json_object",
    "json_objectagg",
    "json_query",
    "json_table",
    "json_table_primitive",
    "json_value",
    "lag",
    "language",
    "large",
    "last_value",
    "lateral",
    "lead",
    "leading",
    "left",
    "like",
    "like_regex",
    "listagg",
    "ln",
    "local",
    "localtime",
    "localtimestamp",
    "log",
    "log10",
    "lower",
    "match",
    "match_number",
    "match_recognize",
    "matches",
    "max",
    "member",
    "merge",
    "method",
    "min",
    "minute",
    "mod",
    "modifies",
    "module",
    "month",
    "multiset",
    "national",
    "natural",
    "nchar",
    "nclob",
    "new",
    "no",
    "none",
    "normalize",
    "not",
    "nth_value",
    "ntile",
    "null",
    "nullif",
    "numeric",
    "octet_length",
    "occurrences_regex",
    "of",
    "offset",
    "old",
    "omit",
    "on",
    "one",
    "only",
    "open",
    "or",
    "order",
    "out",
    "outer",
    "over",
    "overlaps",
    "overlay",
    "parameter",
    "partition",
    "pattern",
    "per",
    "percent",
    "percent_rank",
    "percentile_cont",
    "percentile_disc",
    "period",
    "portion",
    "position",
    "position_regex",
    "power",
    "precedes",
    "precision",
    "prepare",
    "primary",
    "procedure",
    "ptf",
    "range",
    "rank",
    "reads",
    "real",
    "recursive",
    "ref",
    "references",
    "referencing",
    "regr_avgx",
    "regr_avgy",
    "regr_count",
    "regr_intercept",
    "regr_r2",
    "regr_slope",
    "regr_sxx",
    "regr_sxy",
    "regr_syy",
    "release",
    "result",
    "return",
    "returns",
    "revoke",
    "right",
    "rollback",
    "rollup",
    "row",
    "row_number",
    "rows",
    "running",
    "savepoint",
    "scope",
    "scroll",
    "search",
    "second",
    "seek",
    "select",
    "sensitive",
    "session_user",
    "set",
    "show",
    "similar",
    "sin",
    "sinh",
    "skip",
    "smallint",
    "some",
    "specific",
    "specifictype",
    "sql",
    "sqlexception",
    "sqlstate",
    "sqlwarning",
    "sqrt",
    "start",
    "static",
    "stddev_pop",
    "stddev_samp",
    "submultiset",
    "subset",
    "substring",
    "substring_regex",
    "succeeds",
    "sum",
    "symmetric",
    "system",
    "system_time",
    "system_user",
    "table",
    "tablesample",
    "tan",
    "tanh",
    "then",
    "time",
    "timestamp",
    "timezone_hour",
    "timezone_minute",
    "to",
    "trailing",
    "translate",
    "translate_regex",
    "translation",
    "treat",
    "trigger",
    "trim",
    "trim_array",
    "true",
    "truncate",
    "uescape",
    "union",
    "unique",
    "unknown",
    "unnest",
    "update   ",
    "upper",
    "user",
    "using",
    "value",
    "values",
    "value_of",
    "var_pop",
    "var_samp",
    "varbinary",
    "varchar",
    "varying",
    "versioning",
    "when",
    "whenever",
    "where",
    "width_bucket",
    "window",
    "with",
    "within",
    "without",
    "year",
  ];

  // these are reserved words we have identified to be functions
  // and should only be highlighted in a dispatch-like context
  // ie, array_agg(...), etc.
  const RESERVED_FUNCTIONS = [
    "abs",
    "acos",
    "array_agg",
    "asin",
    "atan",
    "avg",
    "cast",
    "ceil",
    "ceiling",
    "coalesce",
    "corr",
    "cos",
    "cosh",
    "count",
    "covar_pop",
    "covar_samp",
    "cume_dist",
    "dense_rank",
    "deref",
    "element",
    "exp",
    "extract",
    "first_value",
    "floor",
    "json_array",
    "json_arrayagg",
    "json_exists",
    "json_object",
    "json_objectagg",
    "json_query",
    "json_table",
    "json_table_primitive",
    "json_value",
    "lag",
    "last_value",
    "lead",
    "listagg",
    "ln",
    "log",
    "log10",
    "lower",
    "max",
    "min",
    "mod",
    "nth_value",
    "ntile",
    "nullif",
    "percent_rank",
    "percentile_cont",
    "percentile_disc",
    "position",
    "position_regex",
    "power",
    "rank",
    "regr_avgx",
    "regr_avgy",
    "regr_count",
    "regr_intercept",
    "regr_r2",
    "regr_slope",
    "regr_sxx",
    "regr_sxy",
    "regr_syy",
    "row_number",
    "sin",
    "sinh",
    "sqrt",
    "stddev_pop",
    "stddev_samp",
    "substring",
    "substring_regex",
    "sum",
    "tan",
    "tanh",
    "translate",
    "translate_regex",
    "treat",
    "trim",
    "trim_array",
    "unnest",
    "upper",
    "value_of",
    "var_pop",
    "var_samp",
    "width_bucket",
  ];

  // these functions can
  const POSSIBLE_WITHOUT_PARENS = [
    "current_catalog",
    "current_date",
    "current_default_transform_group",
    "current_path",
    "current_role",
    "current_schema",
    "current_transform_group_for_type",
    "current_user",
    "session_user",
    "system_time",
    "system_user",
    "current_time",
    "localtime",
    "current_timestamp",
    "localtimestamp"
  ];

  // those exist to boost relevance making these very
  // "SQL like" keyword combos worth +1 extra relevance
  const COMBOS = [
    "create table",
    "insert into",
    "primary key",
    "foreign key",
    "not null",
    "alter table",
    "add constraint",
    "grouping sets",
    "on overflow",
    "character set",
    "respect nulls",
    "ignore nulls",
    "nulls first",
    "nulls last",
    "depth first",
    "breadth first"
  ];

  const FUNCTIONS = RESERVED_FUNCTIONS;

  const KEYWORDS = [...RESERVED_WORDS, ...NON_RESERVED_WORDS].filter((keyword) => {
    return !RESERVED_FUNCTIONS.includes(keyword);
  });

  const VARIABLE = {
    className: "variable",
    begin: /@[a-z0-9]+/,
  };

  const OPERATOR = {
    className: "operator",
    begin: /[-+*/=%^~]|&&?|\|\|?|!=?|<(?:=>?|<|>)?|>[>=]?/,
    relevance: 0,
  };

  const FUNCTION_CALL = {
    begin: concat(/\b/, either(...FUNCTIONS), /\s*\(/),
    keywords: {
      built_in: FUNCTIONS
    }
  };

  // keywords with less than 3 letters are reduced in relevancy
  function reduceRelevancy(list, {exceptions, when} = {}) {
    const qualifyFn = when;
    exceptions = exceptions || [];
    return list.map((item) => {
      if (item.match(/\|\d+$/) || exceptions.includes(item)) {
        return item;
      } else if (qualifyFn(item)) {
        return `${item}|0`;
      } else {
        return item;
      }
    });
  }

  return {
    name: 'SQL',
    case_insensitive: true,
    // does not include {} or HTML tags `</`
    illegal: /[{}]|<\//,
    keywords: {
      $pattern: /\b[\w\.]+/,
      keyword:
        reduceRelevancy(KEYWORDS, { when: (x) => x.length < 3 }),
      literal: LITERALS,
      type: TYPES,
      built_in: POSSIBLE_WITHOUT_PARENS
    },
    contains: [
      {
        begin: either(...COMBOS),
        keywords: {
          $pattern: /[\w\.]+/,
          keyword: KEYWORDS.concat(COMBOS),
          literal: LITERALS,
          type: TYPES
        },
      },
      {
        className: "type",
        begin: either(...MULTI_WORD_TYPES)
      },
      FUNCTION_CALL,
      VARIABLE,
      STRING,
      QUOTED_IDENTIFIER,
      hljs.C_NUMBER_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      COMMENT_MODE,
      OPERATOR
    ]
  };
}

module.exports = sql;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc3FsLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0EsV0FBVyxRQUFRO0FBQ25CLGFBQWE7QUFDYjs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyx1QkFBdUI7QUFDbEMsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXLHNCQUFzQjtBQUNqQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQixjQUFjO0FBQ2hDOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBLEdBQUc7O0FBRUg7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQSxrQ0FBa0Msa0JBQWtCLElBQUk7QUFDeEQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFFBQVE7QUFDUixrQkFBa0IsS0FBSztBQUN2QixRQUFRO0FBQ1I7QUFDQTtBQUNBLEtBQUs7QUFDTDs7QUFFQTtBQUNBO0FBQ0E7QUFDQSwyQkFBMkI7QUFDM0IsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBLG9DQUFvQywyQkFBMkI7QUFDL0Q7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1QsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9zcWwuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHsuLi4oUmVnRXhwIHwgc3RyaW5nKSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGNvbmNhdCguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9IGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJcIik7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qKlxuICogQW55IG9mIHRoZSBwYXNzZWQgZXhwcmVzc3Npb25zIG1heSBtYXRjaFxuICpcbiAqIENyZWF0ZXMgYSBodWdlIHRoaXMgfCB0aGlzIHwgdGhhdCB8IHRoYXQgbWF0Y2hcbiAqIEBwYXJhbSB7KFJlZ0V4cCB8IHN0cmluZylbXSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGVpdGhlciguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9ICcoJyArIGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJ8XCIpICsgXCIpXCI7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qXG4gTGFuZ3VhZ2U6IFNRTFxuIFdlYnNpdGU6IGh0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy93aWtpL1NRTFxuIENhdGVnb3J5OiBjb21tb24sIGRhdGFiYXNlXG4gKi9cblxuZnVuY3Rpb24gc3FsKGhsanMpIHtcbiAgY29uc3QgQ09NTUVOVF9NT0RFID0gaGxqcy5DT01NRU5UKCctLScsICckJyk7XG4gIGNvbnN0IFNUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvJy8sXG4gICAgICAgIGVuZDogLycvLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtiZWdpbjogLycnLyB9XG4gICAgICAgIF1cbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIGNvbnN0IFFVT1RFRF9JREVOVElGSUVSID0ge1xuICAgIGJlZ2luOiAvXCIvLFxuICAgIGVuZDogL1wiLyxcbiAgICBjb250YWluczogWyB7IGJlZ2luOiAvXCJcIi8gfSBdXG4gIH07XG5cbiAgY29uc3QgTElURVJBTFMgPSBbXG4gICAgXCJ0cnVlXCIsXG4gICAgXCJmYWxzZVwiLFxuICAgIC8vIE5vdCBzdXJlIGl0J3MgY29ycmVjdCB0byBjYWxsIE5VTEwgbGl0ZXJhbCwgYW5kIGNsYXVzZXMgbGlrZSBJUyBbTk9UXSBOVUxMIGxvb2sgc3RyYW5nZSB0aGF0IHdheS5cbiAgICAvLyBcIm51bGxcIixcbiAgICBcInVua25vd25cIlxuICBdO1xuXG4gIGNvbnN0IE1VTFRJX1dPUkRfVFlQRVMgPSBbXG4gICAgXCJkb3VibGUgcHJlY2lzaW9uXCIsXG4gICAgXCJsYXJnZSBvYmplY3RcIixcbiAgICBcIndpdGggdGltZXpvbmVcIixcbiAgICBcIndpdGhvdXQgdGltZXpvbmVcIlxuICBdO1xuXG4gIGNvbnN0IFRZUEVTID0gW1xuICAgICdiaWdpbnQnLFxuICAgICdiaW5hcnknLFxuICAgICdibG9iJyxcbiAgICAnYm9vbGVhbicsXG4gICAgJ2NoYXInLFxuICAgICdjaGFyYWN0ZXInLFxuICAgICdjbG9iJyxcbiAgICAnZGF0ZScsXG4gICAgJ2RlYycsXG4gICAgJ2RlY2Zsb2F0JyxcbiAgICAnZGVjaW1hbCcsXG4gICAgJ2Zsb2F0JyxcbiAgICAnaW50JyxcbiAgICAnaW50ZWdlcicsXG4gICAgJ2ludGVydmFsJyxcbiAgICAnbmNoYXInLFxuICAgICduY2xvYicsXG4gICAgJ25hdGlvbmFsJyxcbiAgICAnbnVtZXJpYycsXG4gICAgJ3JlYWwnLFxuICAgICdyb3cnLFxuICAgICdzbWFsbGludCcsXG4gICAgJ3RpbWUnLFxuICAgICd0aW1lc3RhbXAnLFxuICAgICd2YXJjaGFyJyxcbiAgICAndmFyeWluZycsIC8vIG1vZGlmaWVyIChjaGFyYWN0ZXIgdmFyeWluZylcbiAgICAndmFyYmluYXJ5J1xuICBdO1xuXG4gIGNvbnN0IE5PTl9SRVNFUlZFRF9XT1JEUyA9IFtcbiAgICBcImFkZFwiLFxuICAgIFwiYXNjXCIsXG4gICAgXCJjb2xsYXRpb25cIixcbiAgICBcImRlc2NcIixcbiAgICBcImZpbmFsXCIsXG4gICAgXCJmaXJzdFwiLFxuICAgIFwibGFzdFwiLFxuICAgIFwidmlld1wiXG4gIF07XG5cbiAgLy8gaHR0cHM6Ly9qYWtld2hlYXQuZ2l0aHViLmlvL3NxbC1vdmVydmlldy9zcWwtMjAxNi1mb3VuZGF0aW9uLWdyYW1tYXIuaHRtbCNyZXNlcnZlZC13b3JkXG4gIGNvbnN0IFJFU0VSVkVEX1dPUkRTID0gW1xuICAgIFwiYWJzXCIsXG4gICAgXCJhY29zXCIsXG4gICAgXCJhbGxcIixcbiAgICBcImFsbG9jYXRlXCIsXG4gICAgXCJhbHRlclwiLFxuICAgIFwiYW5kXCIsXG4gICAgXCJhbnlcIixcbiAgICBcImFyZVwiLFxuICAgIFwiYXJyYXlcIixcbiAgICBcImFycmF5X2FnZ1wiLFxuICAgIFwiYXJyYXlfbWF4X2NhcmRpbmFsaXR5XCIsXG4gICAgXCJhc1wiLFxuICAgIFwiYXNlbnNpdGl2ZVwiLFxuICAgIFwiYXNpblwiLFxuICAgIFwiYXN5bW1ldHJpY1wiLFxuICAgIFwiYXRcIixcbiAgICBcImF0YW5cIixcbiAgICBcImF0b21pY1wiLFxuICAgIFwiYXV0aG9yaXphdGlvblwiLFxuICAgIFwiYXZnXCIsXG4gICAgXCJiZWdpblwiLFxuICAgIFwiYmVnaW5fZnJhbWVcIixcbiAgICBcImJlZ2luX3BhcnRpdGlvblwiLFxuICAgIFwiYmV0d2VlblwiLFxuICAgIFwiYmlnaW50XCIsXG4gICAgXCJiaW5hcnlcIixcbiAgICBcImJsb2JcIixcbiAgICBcImJvb2xlYW5cIixcbiAgICBcImJvdGhcIixcbiAgICBcImJ5XCIsXG4gICAgXCJjYWxsXCIsXG4gICAgXCJjYWxsZWRcIixcbiAgICBcImNhcmRpbmFsaXR5XCIsXG4gICAgXCJjYXNjYWRlZFwiLFxuICAgIFwiY2FzZVwiLFxuICAgIFwiY2FzdFwiLFxuICAgIFwiY2VpbFwiLFxuICAgIFwiY2VpbGluZ1wiLFxuICAgIFwiY2hhclwiLFxuICAgIFwiY2hhcl9sZW5ndGhcIixcbiAgICBcImNoYXJhY3RlclwiLFxuICAgIFwiY2hhcmFjdGVyX2xlbmd0aFwiLFxuICAgIFwiY2hlY2tcIixcbiAgICBcImNsYXNzaWZpZXJcIixcbiAgICBcImNsb2JcIixcbiAgICBcImNsb3NlXCIsXG4gICAgXCJjb2FsZXNjZVwiLFxuICAgIFwiY29sbGF0ZVwiLFxuICAgIFwiY29sbGVjdFwiLFxuICAgIFwiY29sdW1uXCIsXG4gICAgXCJjb21taXRcIixcbiAgICBcImNvbmRpdGlvblwiLFxuICAgIFwiY29ubmVjdFwiLFxuICAgIFwiY29uc3RyYWludFwiLFxuICAgIFwiY29udGFpbnNcIixcbiAgICBcImNvbnZlcnRcIixcbiAgICBcImNvcHlcIixcbiAgICBcImNvcnJcIixcbiAgICBcImNvcnJlc3BvbmRpbmdcIixcbiAgICBcImNvc1wiLFxuICAgIFwiY29zaFwiLFxuICAgIFwiY291bnRcIixcbiAgICBcImNvdmFyX3BvcFwiLFxuICAgIFwiY292YXJfc2FtcFwiLFxuICAgIFwiY3JlYXRlXCIsXG4gICAgXCJjcm9zc1wiLFxuICAgIFwiY3ViZVwiLFxuICAgIFwiY3VtZV9kaXN0XCIsXG4gICAgXCJjdXJyZW50XCIsXG4gICAgXCJjdXJyZW50X2NhdGFsb2dcIixcbiAgICBcImN1cnJlbnRfZGF0ZVwiLFxuICAgIFwiY3VycmVudF9kZWZhdWx0X3RyYW5zZm9ybV9ncm91cFwiLFxuICAgIFwiY3VycmVudF9wYXRoXCIsXG4gICAgXCJjdXJyZW50X3JvbGVcIixcbiAgICBcImN1cnJlbnRfcm93XCIsXG4gICAgXCJjdXJyZW50X3NjaGVtYVwiLFxuICAgIFwiY3VycmVudF90aW1lXCIsXG4gICAgXCJjdXJyZW50X3RpbWVzdGFtcFwiLFxuICAgIFwiY3VycmVudF9wYXRoXCIsXG4gICAgXCJjdXJyZW50X3JvbGVcIixcbiAgICBcImN1cnJlbnRfdHJhbnNmb3JtX2dyb3VwX2Zvcl90eXBlXCIsXG4gICAgXCJjdXJyZW50X3VzZXJcIixcbiAgICBcImN1cnNvclwiLFxuICAgIFwiY3ljbGVcIixcbiAgICBcImRhdGVcIixcbiAgICBcImRheVwiLFxuICAgIFwiZGVhbGxvY2F0ZVwiLFxuICAgIFwiZGVjXCIsXG4gICAgXCJkZWNpbWFsXCIsXG4gICAgXCJkZWNmbG9hdFwiLFxuICAgIFwiZGVjbGFyZVwiLFxuICAgIFwiZGVmYXVsdFwiLFxuICAgIFwiZGVmaW5lXCIsXG4gICAgXCJkZWxldGVcIixcbiAgICBcImRlbnNlX3JhbmtcIixcbiAgICBcImRlcmVmXCIsXG4gICAgXCJkZXNjcmliZVwiLFxuICAgIFwiZGV0ZXJtaW5pc3RpY1wiLFxuICAgIFwiZGlzY29ubmVjdFwiLFxuICAgIFwiZGlzdGluY3RcIixcbiAgICBcImRvdWJsZVwiLFxuICAgIFwiZHJvcFwiLFxuICAgIFwiZHluYW1pY1wiLFxuICAgIFwiZWFjaFwiLFxuICAgIFwiZWxlbWVudFwiLFxuICAgIFwiZWxzZVwiLFxuICAgIFwiZW1wdHlcIixcbiAgICBcImVuZFwiLFxuICAgIFwiZW5kX2ZyYW1lXCIsXG4gICAgXCJlbmRfcGFydGl0aW9uXCIsXG4gICAgXCJlbmQtZXhlY1wiLFxuICAgIFwiZXF1YWxzXCIsXG4gICAgXCJlc2NhcGVcIixcbiAgICBcImV2ZXJ5XCIsXG4gICAgXCJleGNlcHRcIixcbiAgICBcImV4ZWNcIixcbiAgICBcImV4ZWN1dGVcIixcbiAgICBcImV4aXN0c1wiLFxuICAgIFwiZXhwXCIsXG4gICAgXCJleHRlcm5hbFwiLFxuICAgIFwiZXh0cmFjdFwiLFxuICAgIFwiZmFsc2VcIixcbiAgICBcImZldGNoXCIsXG4gICAgXCJmaWx0ZXJcIixcbiAgICBcImZpcnN0X3ZhbHVlXCIsXG4gICAgXCJmbG9hdFwiLFxuICAgIFwiZmxvb3JcIixcbiAgICBcImZvclwiLFxuICAgIFwiZm9yZWlnblwiLFxuICAgIFwiZnJhbWVfcm93XCIsXG4gICAgXCJmcmVlXCIsXG4gICAgXCJmcm9tXCIsXG4gICAgXCJmdWxsXCIsXG4gICAgXCJmdW5jdGlvblwiLFxuICAgIFwiZnVzaW9uXCIsXG4gICAgXCJnZXRcIixcbiAgICBcImdsb2JhbFwiLFxuICAgIFwiZ3JhbnRcIixcbiAgICBcImdyb3VwXCIsXG4gICAgXCJncm91cGluZ1wiLFxuICAgIFwiZ3JvdXBzXCIsXG4gICAgXCJoYXZpbmdcIixcbiAgICBcImhvbGRcIixcbiAgICBcImhvdXJcIixcbiAgICBcImlkZW50aXR5XCIsXG4gICAgXCJpblwiLFxuICAgIFwiaW5kaWNhdG9yXCIsXG4gICAgXCJpbml0aWFsXCIsXG4gICAgXCJpbm5lclwiLFxuICAgIFwiaW5vdXRcIixcbiAgICBcImluc2Vuc2l0aXZlXCIsXG4gICAgXCJpbnNlcnRcIixcbiAgICBcImludFwiLFxuICAgIFwiaW50ZWdlclwiLFxuICAgIFwiaW50ZXJzZWN0XCIsXG4gICAgXCJpbnRlcnNlY3Rpb25cIixcbiAgICBcImludGVydmFsXCIsXG4gICAgXCJpbnRvXCIsXG4gICAgXCJpc1wiLFxuICAgIFwiam9pblwiLFxuICAgIFwianNvbl9hcnJheVwiLFxuICAgIFwianNvbl9hcnJheWFnZ1wiLFxuICAgIFwianNvbl9leGlzdHNcIixcbiAgICBcImpzb25fb2JqZWN0XCIsXG4gICAgXCJqc29uX29iamVjdGFnZ1wiLFxuICAgIFwianNvbl9xdWVyeVwiLFxuICAgIFwianNvbl90YWJsZVwiLFxuICAgIFwianNvbl90YWJsZV9wcmltaXRpdmVcIixcbiAgICBcImpzb25fdmFsdWVcIixcbiAgICBcImxhZ1wiLFxuICAgIFwibGFuZ3VhZ2VcIixcbiAgICBcImxhcmdlXCIsXG4gICAgXCJsYXN0X3ZhbHVlXCIsXG4gICAgXCJsYXRlcmFsXCIsXG4gICAgXCJsZWFkXCIsXG4gICAgXCJsZWFkaW5nXCIsXG4gICAgXCJsZWZ0XCIsXG4gICAgXCJsaWtlXCIsXG4gICAgXCJsaWtlX3JlZ2V4XCIsXG4gICAgXCJsaXN0YWdnXCIsXG4gICAgXCJsblwiLFxuICAgIFwibG9jYWxcIixcbiAgICBcImxvY2FsdGltZVwiLFxuICAgIFwibG9jYWx0aW1lc3RhbXBcIixcbiAgICBcImxvZ1wiLFxuICAgIFwibG9nMTBcIixcbiAgICBcImxvd2VyXCIsXG4gICAgXCJtYXRjaFwiLFxuICAgIFwibWF0Y2hfbnVtYmVyXCIsXG4gICAgXCJtYXRjaF9yZWNvZ25pemVcIixcbiAgICBcIm1hdGNoZXNcIixcbiAgICBcIm1heFwiLFxuICAgIFwibWVtYmVyXCIsXG4gICAgXCJtZXJnZVwiLFxuICAgIFwibWV0aG9kXCIsXG4gICAgXCJtaW5cIixcbiAgICBcIm1pbnV0ZVwiLFxuICAgIFwibW9kXCIsXG4gICAgXCJtb2RpZmllc1wiLFxuICAgIFwibW9kdWxlXCIsXG4gICAgXCJtb250aFwiLFxuICAgIFwibXVsdGlzZXRcIixcbiAgICBcIm5hdGlvbmFsXCIsXG4gICAgXCJuYXR1cmFsXCIsXG4gICAgXCJuY2hhclwiLFxuICAgIFwibmNsb2JcIixcbiAgICBcIm5ld1wiLFxuICAgIFwibm9cIixcbiAgICBcIm5vbmVcIixcbiAgICBcIm5vcm1hbGl6ZVwiLFxuICAgIFwibm90XCIsXG4gICAgXCJudGhfdmFsdWVcIixcbiAgICBcIm50aWxlXCIsXG4gICAgXCJudWxsXCIsXG4gICAgXCJudWxsaWZcIixcbiAgICBcIm51bWVyaWNcIixcbiAgICBcIm9jdGV0X2xlbmd0aFwiLFxuICAgIFwib2NjdXJyZW5jZXNfcmVnZXhcIixcbiAgICBcIm9mXCIsXG4gICAgXCJvZmZzZXRcIixcbiAgICBcIm9sZFwiLFxuICAgIFwib21pdFwiLFxuICAgIFwib25cIixcbiAgICBcIm9uZVwiLFxuICAgIFwib25seVwiLFxuICAgIFwib3BlblwiLFxuICAgIFwib3JcIixcbiAgICBcIm9yZGVyXCIsXG4gICAgXCJvdXRcIixcbiAgICBcIm91dGVyXCIsXG4gICAgXCJvdmVyXCIsXG4gICAgXCJvdmVybGFwc1wiLFxuICAgIFwib3ZlcmxheVwiLFxuICAgIFwicGFyYW1ldGVyXCIsXG4gICAgXCJwYXJ0aXRpb25cIixcbiAgICBcInBhdHRlcm5cIixcbiAgICBcInBlclwiLFxuICAgIFwicGVyY2VudFwiLFxuICAgIFwicGVyY2VudF9yYW5rXCIsXG4gICAgXCJwZXJjZW50aWxlX2NvbnRcIixcbiAgICBcInBlcmNlbnRpbGVfZGlzY1wiLFxuICAgIFwicGVyaW9kXCIsXG4gICAgXCJwb3J0aW9uXCIsXG4gICAgXCJwb3NpdGlvblwiLFxuICAgIFwicG9zaXRpb25fcmVnZXhcIixcbiAgICBcInBvd2VyXCIsXG4gICAgXCJwcmVjZWRlc1wiLFxuICAgIFwicHJlY2lzaW9uXCIsXG4gICAgXCJwcmVwYXJlXCIsXG4gICAgXCJwcmltYXJ5XCIsXG4gICAgXCJwcm9jZWR1cmVcIixcbiAgICBcInB0ZlwiLFxuICAgIFwicmFuZ2VcIixcbiAgICBcInJhbmtcIixcbiAgICBcInJlYWRzXCIsXG4gICAgXCJyZWFsXCIsXG4gICAgXCJyZWN1cnNpdmVcIixcbiAgICBcInJlZlwiLFxuICAgIFwicmVmZXJlbmNlc1wiLFxuICAgIFwicmVmZXJlbmNpbmdcIixcbiAgICBcInJlZ3JfYXZneFwiLFxuICAgIFwicmVncl9hdmd5XCIsXG4gICAgXCJyZWdyX2NvdW50XCIsXG4gICAgXCJyZWdyX2ludGVyY2VwdFwiLFxuICAgIFwicmVncl9yMlwiLFxuICAgIFwicmVncl9zbG9wZVwiLFxuICAgIFwicmVncl9zeHhcIixcbiAgICBcInJlZ3Jfc3h5XCIsXG4gICAgXCJyZWdyX3N5eVwiLFxuICAgIFwicmVsZWFzZVwiLFxuICAgIFwicmVzdWx0XCIsXG4gICAgXCJyZXR1cm5cIixcbiAgICBcInJldHVybnNcIixcbiAgICBcInJldm9rZVwiLFxuICAgIFwicmlnaHRcIixcbiAgICBcInJvbGxiYWNrXCIsXG4gICAgXCJyb2xsdXBcIixcbiAgICBcInJvd1wiLFxuICAgIFwicm93X251bWJlclwiLFxuICAgIFwicm93c1wiLFxuICAgIFwicnVubmluZ1wiLFxuICAgIFwic2F2ZXBvaW50XCIsXG4gICAgXCJzY29wZVwiLFxuICAgIFwic2Nyb2xsXCIsXG4gICAgXCJzZWFyY2hcIixcbiAgICBcInNlY29uZFwiLFxuICAgIFwic2Vla1wiLFxuICAgIFwic2VsZWN0XCIsXG4gICAgXCJzZW5zaXRpdmVcIixcbiAgICBcInNlc3Npb25fdXNlclwiLFxuICAgIFwic2V0XCIsXG4gICAgXCJzaG93XCIsXG4gICAgXCJzaW1pbGFyXCIsXG4gICAgXCJzaW5cIixcbiAgICBcInNpbmhcIixcbiAgICBcInNraXBcIixcbiAgICBcInNtYWxsaW50XCIsXG4gICAgXCJzb21lXCIsXG4gICAgXCJzcGVjaWZpY1wiLFxuICAgIFwic3BlY2lmaWN0eXBlXCIsXG4gICAgXCJzcWxcIixcbiAgICBcInNxbGV4Y2VwdGlvblwiLFxuICAgIFwic3Fsc3RhdGVcIixcbiAgICBcInNxbHdhcm5pbmdcIixcbiAgICBcInNxcnRcIixcbiAgICBcInN0YXJ0XCIsXG4gICAgXCJzdGF0aWNcIixcbiAgICBcInN0ZGRldl9wb3BcIixcbiAgICBcInN0ZGRldl9zYW1wXCIsXG4gICAgXCJzdWJtdWx0aXNldFwiLFxuICAgIFwic3Vic2V0XCIsXG4gICAgXCJzdWJzdHJpbmdcIixcbiAgICBcInN1YnN0cmluZ19yZWdleFwiLFxuICAgIFwic3VjY2VlZHNcIixcbiAgICBcInN1bVwiLFxuICAgIFwic3ltbWV0cmljXCIsXG4gICAgXCJzeXN0ZW1cIixcbiAgICBcInN5c3RlbV90aW1lXCIsXG4gICAgXCJzeXN0ZW1fdXNlclwiLFxuICAgIFwidGFibGVcIixcbiAgICBcInRhYmxlc2FtcGxlXCIsXG4gICAgXCJ0YW5cIixcbiAgICBcInRhbmhcIixcbiAgICBcInRoZW5cIixcbiAgICBcInRpbWVcIixcbiAgICBcInRpbWVzdGFtcFwiLFxuICAgIFwidGltZXpvbmVfaG91clwiLFxuICAgIFwidGltZXpvbmVfbWludXRlXCIsXG4gICAgXCJ0b1wiLFxuICAgIFwidHJhaWxpbmdcIixcbiAgICBcInRyYW5zbGF0ZVwiLFxuICAgIFwidHJhbnNsYXRlX3JlZ2V4XCIsXG4gICAgXCJ0cmFuc2xhdGlvblwiLFxuICAgIFwidHJlYXRcIixcbiAgICBcInRyaWdnZXJcIixcbiAgICBcInRyaW1cIixcbiAgICBcInRyaW1fYXJyYXlcIixcbiAgICBcInRydWVcIixcbiAgICBcInRydW5jYXRlXCIsXG4gICAgXCJ1ZXNjYXBlXCIsXG4gICAgXCJ1bmlvblwiLFxuICAgIFwidW5pcXVlXCIsXG4gICAgXCJ1bmtub3duXCIsXG4gICAgXCJ1bm5lc3RcIixcbiAgICBcInVwZGF0ZSAgIFwiLFxuICAgIFwidXBwZXJcIixcbiAgICBcInVzZXJcIixcbiAgICBcInVzaW5nXCIsXG4gICAgXCJ2YWx1ZVwiLFxuICAgIFwidmFsdWVzXCIsXG4gICAgXCJ2YWx1ZV9vZlwiLFxuICAgIFwidmFyX3BvcFwiLFxuICAgIFwidmFyX3NhbXBcIixcbiAgICBcInZhcmJpbmFyeVwiLFxuICAgIFwidmFyY2hhclwiLFxuICAgIFwidmFyeWluZ1wiLFxuICAgIFwidmVyc2lvbmluZ1wiLFxuICAgIFwid2hlblwiLFxuICAgIFwid2hlbmV2ZXJcIixcbiAgICBcIndoZXJlXCIsXG4gICAgXCJ3aWR0aF9idWNrZXRcIixcbiAgICBcIndpbmRvd1wiLFxuICAgIFwid2l0aFwiLFxuICAgIFwid2l0aGluXCIsXG4gICAgXCJ3aXRob3V0XCIsXG4gICAgXCJ5ZWFyXCIsXG4gIF07XG5cbiAgLy8gdGhlc2UgYXJlIHJlc2VydmVkIHdvcmRzIHdlIGhhdmUgaWRlbnRpZmllZCB0byBiZSBmdW5jdGlvbnNcbiAgLy8gYW5kIHNob3VsZCBvbmx5IGJlIGhpZ2hsaWdodGVkIGluIGEgZGlzcGF0Y2gtbGlrZSBjb250ZXh0XG4gIC8vIGllLCBhcnJheV9hZ2coLi4uKSwgZXRjLlxuICBjb25zdCBSRVNFUlZFRF9GVU5DVElPTlMgPSBbXG4gICAgXCJhYnNcIixcbiAgICBcImFjb3NcIixcbiAgICBcImFycmF5X2FnZ1wiLFxuICAgIFwiYXNpblwiLFxuICAgIFwiYXRhblwiLFxuICAgIFwiYXZnXCIsXG4gICAgXCJjYXN0XCIsXG4gICAgXCJjZWlsXCIsXG4gICAgXCJjZWlsaW5nXCIsXG4gICAgXCJjb2FsZXNjZVwiLFxuICAgIFwiY29yclwiLFxuICAgIFwiY29zXCIsXG4gICAgXCJjb3NoXCIsXG4gICAgXCJjb3VudFwiLFxuICAgIFwiY292YXJfcG9wXCIsXG4gICAgXCJjb3Zhcl9zYW1wXCIsXG4gICAgXCJjdW1lX2Rpc3RcIixcbiAgICBcImRlbnNlX3JhbmtcIixcbiAgICBcImRlcmVmXCIsXG4gICAgXCJlbGVtZW50XCIsXG4gICAgXCJleHBcIixcbiAgICBcImV4dHJhY3RcIixcbiAgICBcImZpcnN0X3ZhbHVlXCIsXG4gICAgXCJmbG9vclwiLFxuICAgIFwianNvbl9hcnJheVwiLFxuICAgIFwianNvbl9hcnJheWFnZ1wiLFxuICAgIFwianNvbl9leGlzdHNcIixcbiAgICBcImpzb25fb2JqZWN0XCIsXG4gICAgXCJqc29uX29iamVjdGFnZ1wiLFxuICAgIFwianNvbl9xdWVyeVwiLFxuICAgIFwianNvbl90YWJsZVwiLFxuICAgIFwianNvbl90YWJsZV9wcmltaXRpdmVcIixcbiAgICBcImpzb25fdmFsdWVcIixcbiAgICBcImxhZ1wiLFxuICAgIFwibGFzdF92YWx1ZVwiLFxuICAgIFwibGVhZFwiLFxuICAgIFwibGlzdGFnZ1wiLFxuICAgIFwibG5cIixcbiAgICBcImxvZ1wiLFxuICAgIFwibG9nMTBcIixcbiAgICBcImxvd2VyXCIsXG4gICAgXCJtYXhcIixcbiAgICBcIm1pblwiLFxuICAgIFwibW9kXCIsXG4gICAgXCJudGhfdmFsdWVcIixcbiAgICBcIm50aWxlXCIsXG4gICAgXCJudWxsaWZcIixcbiAgICBcInBlcmNlbnRfcmFua1wiLFxuICAgIFwicGVyY2VudGlsZV9jb250XCIsXG4gICAgXCJwZXJjZW50aWxlX2Rpc2NcIixcbiAgICBcInBvc2l0aW9uXCIsXG4gICAgXCJwb3NpdGlvbl9yZWdleFwiLFxuICAgIFwicG93ZXJcIixcbiAgICBcInJhbmtcIixcbiAgICBcInJlZ3JfYXZneFwiLFxuICAgIFwicmVncl9hdmd5XCIsXG4gICAgXCJyZWdyX2NvdW50XCIsXG4gICAgXCJyZWdyX2ludGVyY2VwdFwiLFxuICAgIFwicmVncl9yMlwiLFxuICAgIFwicmVncl9zbG9wZVwiLFxuICAgIFwicmVncl9zeHhcIixcbiAgICBcInJlZ3Jfc3h5XCIsXG4gICAgXCJyZWdyX3N5eVwiLFxuICAgIFwicm93X251bWJlclwiLFxuICAgIFwic2luXCIsXG4gICAgXCJzaW5oXCIsXG4gICAgXCJzcXJ0XCIsXG4gICAgXCJzdGRkZXZfcG9wXCIsXG4gICAgXCJzdGRkZXZfc2FtcFwiLFxuICAgIFwic3Vic3RyaW5nXCIsXG4gICAgXCJzdWJzdHJpbmdfcmVnZXhcIixcbiAgICBcInN1bVwiLFxuICAgIFwidGFuXCIsXG4gICAgXCJ0YW5oXCIsXG4gICAgXCJ0cmFuc2xhdGVcIixcbiAgICBcInRyYW5zbGF0ZV9yZWdleFwiLFxuICAgIFwidHJlYXRcIixcbiAgICBcInRyaW1cIixcbiAgICBcInRyaW1fYXJyYXlcIixcbiAgICBcInVubmVzdFwiLFxuICAgIFwidXBwZXJcIixcbiAgICBcInZhbHVlX29mXCIsXG4gICAgXCJ2YXJfcG9wXCIsXG4gICAgXCJ2YXJfc2FtcFwiLFxuICAgIFwid2lkdGhfYnVja2V0XCIsXG4gIF07XG5cbiAgLy8gdGhlc2UgZnVuY3Rpb25zIGNhblxuICBjb25zdCBQT1NTSUJMRV9XSVRIT1VUX1BBUkVOUyA9IFtcbiAgICBcImN1cnJlbnRfY2F0YWxvZ1wiLFxuICAgIFwiY3VycmVudF9kYXRlXCIsXG4gICAgXCJjdXJyZW50X2RlZmF1bHRfdHJhbnNmb3JtX2dyb3VwXCIsXG4gICAgXCJjdXJyZW50X3BhdGhcIixcbiAgICBcImN1cnJlbnRfcm9sZVwiLFxuICAgIFwiY3VycmVudF9zY2hlbWFcIixcbiAgICBcImN1cnJlbnRfdHJhbnNmb3JtX2dyb3VwX2Zvcl90eXBlXCIsXG4gICAgXCJjdXJyZW50X3VzZXJcIixcbiAgICBcInNlc3Npb25fdXNlclwiLFxuICAgIFwic3lzdGVtX3RpbWVcIixcbiAgICBcInN5c3RlbV91c2VyXCIsXG4gICAgXCJjdXJyZW50X3RpbWVcIixcbiAgICBcImxvY2FsdGltZVwiLFxuICAgIFwiY3VycmVudF90aW1lc3RhbXBcIixcbiAgICBcImxvY2FsdGltZXN0YW1wXCJcbiAgXTtcblxuICAvLyB0aG9zZSBleGlzdCB0byBib29zdCByZWxldmFuY2UgbWFraW5nIHRoZXNlIHZlcnlcbiAgLy8gXCJTUUwgbGlrZVwiIGtleXdvcmQgY29tYm9zIHdvcnRoICsxIGV4dHJhIHJlbGV2YW5jZVxuICBjb25zdCBDT01CT1MgPSBbXG4gICAgXCJjcmVhdGUgdGFibGVcIixcbiAgICBcImluc2VydCBpbnRvXCIsXG4gICAgXCJwcmltYXJ5IGtleVwiLFxuICAgIFwiZm9yZWlnbiBrZXlcIixcbiAgICBcIm5vdCBudWxsXCIsXG4gICAgXCJhbHRlciB0YWJsZVwiLFxuICAgIFwiYWRkIGNvbnN0cmFpbnRcIixcbiAgICBcImdyb3VwaW5nIHNldHNcIixcbiAgICBcIm9uIG92ZXJmbG93XCIsXG4gICAgXCJjaGFyYWN0ZXIgc2V0XCIsXG4gICAgXCJyZXNwZWN0IG51bGxzXCIsXG4gICAgXCJpZ25vcmUgbnVsbHNcIixcbiAgICBcIm51bGxzIGZpcnN0XCIsXG4gICAgXCJudWxscyBsYXN0XCIsXG4gICAgXCJkZXB0aCBmaXJzdFwiLFxuICAgIFwiYnJlYWR0aCBmaXJzdFwiXG4gIF07XG5cbiAgY29uc3QgRlVOQ1RJT05TID0gUkVTRVJWRURfRlVOQ1RJT05TO1xuXG4gIGNvbnN0IEtFWVdPUkRTID0gWy4uLlJFU0VSVkVEX1dPUkRTLCAuLi5OT05fUkVTRVJWRURfV09SRFNdLmZpbHRlcigoa2V5d29yZCkgPT4ge1xuICAgIHJldHVybiAhUkVTRVJWRURfRlVOQ1RJT05TLmluY2x1ZGVzKGtleXdvcmQpO1xuICB9KTtcblxuICBjb25zdCBWQVJJQUJMRSA9IHtcbiAgICBjbGFzc05hbWU6IFwidmFyaWFibGVcIixcbiAgICBiZWdpbjogL0BbYS16MC05XSsvLFxuICB9O1xuXG4gIGNvbnN0IE9QRVJBVE9SID0ge1xuICAgIGNsYXNzTmFtZTogXCJvcGVyYXRvclwiLFxuICAgIGJlZ2luOiAvWy0rKi89JV5+XXwmJj98XFx8XFx8P3whPT98PCg/Oj0+P3w8fD4pP3w+Wz49XT8vLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgfTtcblxuICBjb25zdCBGVU5DVElPTl9DQUxMID0ge1xuICAgIGJlZ2luOiBjb25jYXQoL1xcYi8sIGVpdGhlciguLi5GVU5DVElPTlMpLCAvXFxzKlxcKC8pLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBidWlsdF9pbjogRlVOQ1RJT05TXG4gICAgfVxuICB9O1xuXG4gIC8vIGtleXdvcmRzIHdpdGggbGVzcyB0aGFuIDMgbGV0dGVycyBhcmUgcmVkdWNlZCBpbiByZWxldmFuY3lcbiAgZnVuY3Rpb24gcmVkdWNlUmVsZXZhbmN5KGxpc3QsIHtleGNlcHRpb25zLCB3aGVufSA9IHt9KSB7XG4gICAgY29uc3QgcXVhbGlmeUZuID0gd2hlbjtcbiAgICBleGNlcHRpb25zID0gZXhjZXB0aW9ucyB8fCBbXTtcbiAgICByZXR1cm4gbGlzdC5tYXAoKGl0ZW0pID0+IHtcbiAgICAgIGlmIChpdGVtLm1hdGNoKC9cXHxcXGQrJC8pIHx8IGV4Y2VwdGlvbnMuaW5jbHVkZXMoaXRlbSkpIHtcbiAgICAgICAgcmV0dXJuIGl0ZW07XG4gICAgICB9IGVsc2UgaWYgKHF1YWxpZnlGbihpdGVtKSkge1xuICAgICAgICByZXR1cm4gYCR7aXRlbX18MGA7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICByZXR1cm4gaXRlbTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1NRTCcsXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICAvLyBkb2VzIG5vdCBpbmNsdWRlIHt9IG9yIEhUTUwgdGFncyBgPC9gXG4gICAgaWxsZWdhbDogL1t7fV18PFxcLy8sXG4gICAga2V5d29yZHM6IHtcbiAgICAgICRwYXR0ZXJuOiAvXFxiW1xcd1xcLl0rLyxcbiAgICAgIGtleXdvcmQ6XG4gICAgICAgIHJlZHVjZVJlbGV2YW5jeShLRVlXT1JEUywgeyB3aGVuOiAoeCkgPT4geC5sZW5ndGggPCAzIH0pLFxuICAgICAgbGl0ZXJhbDogTElURVJBTFMsXG4gICAgICB0eXBlOiBUWVBFUyxcbiAgICAgIGJ1aWx0X2luOiBQT1NTSUJMRV9XSVRIT1VUX1BBUkVOU1xuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IGVpdGhlciguLi5DT01CT1MpLFxuICAgICAgICBrZXl3b3Jkczoge1xuICAgICAgICAgICRwYXR0ZXJuOiAvW1xcd1xcLl0rLyxcbiAgICAgICAgICBrZXl3b3JkOiBLRVlXT1JEUy5jb25jYXQoQ09NQk9TKSxcbiAgICAgICAgICBsaXRlcmFsOiBMSVRFUkFMUyxcbiAgICAgICAgICB0eXBlOiBUWVBFU1xuICAgICAgICB9LFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiBcInR5cGVcIixcbiAgICAgICAgYmVnaW46IGVpdGhlciguLi5NVUxUSV9XT1JEX1RZUEVTKVxuICAgICAgfSxcbiAgICAgIEZVTkNUSU9OX0NBTEwsXG4gICAgICBWQVJJQUJMRSxcbiAgICAgIFNUUklORyxcbiAgICAgIFFVT1RFRF9JREVOVElGSUVSLFxuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIENPTU1FTlRfTU9ERSxcbiAgICAgIE9QRVJBVE9SXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHNxbDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==