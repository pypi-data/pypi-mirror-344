(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_clojure"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/clojure.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/clojure.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
Language: Clojure
Description: Clojure syntax (based on lisp.js)
Author: mfornos
Website: https://clojure.org
Category: lisp
*/

/** @type LanguageFn */
function clojure(hljs) {
  const SYMBOLSTART = 'a-zA-Z_\\-!.?+*=<>&#\'';
  const SYMBOL_RE = '[' + SYMBOLSTART + '][' + SYMBOLSTART + '0-9/;:]*';
  const globals = 'def defonce defprotocol defstruct defmulti defmethod defn- defn defmacro deftype defrecord';
  const keywords = {
    $pattern: SYMBOL_RE,
    'builtin-name':
      // Clojure keywords
      globals + ' ' +
      'cond apply if-not if-let if not not= =|0 <|0 >|0 <=|0 >=|0 ==|0 +|0 /|0 *|0 -|0 rem ' +
      'quot neg? pos? delay? symbol? keyword? true? false? integer? empty? coll? list? ' +
      'set? ifn? fn? associative? sequential? sorted? counted? reversible? number? decimal? ' +
      'class? distinct? isa? float? rational? reduced? ratio? odd? even? char? seq? vector? ' +
      'string? map? nil? contains? zero? instance? not-every? not-any? libspec? -> ->> .. . ' +
      'inc compare do dotimes mapcat take remove take-while drop letfn drop-last take-last ' +
      'drop-while while intern condp case reduced cycle split-at split-with repeat replicate ' +
      'iterate range merge zipmap declare line-seq sort comparator sort-by dorun doall nthnext ' +
      'nthrest partition eval doseq await await-for let agent atom send send-off release-pending-sends ' +
      'add-watch mapv filterv remove-watch agent-error restart-agent set-error-handler error-handler ' +
      'set-error-mode! error-mode shutdown-agents quote var fn loop recur throw try monitor-enter ' +
      'monitor-exit macroexpand macroexpand-1 for dosync and or ' +
      'when when-not when-let comp juxt partial sequence memoize constantly complement identity assert ' +
      'peek pop doto proxy first rest cons cast coll last butlast ' +
      'sigs reify second ffirst fnext nfirst nnext meta with-meta ns in-ns create-ns import ' +
      'refer keys select-keys vals key val rseq name namespace promise into transient persistent! conj! ' +
      'assoc! dissoc! pop! disj! use class type num float double short byte boolean bigint biginteger ' +
      'bigdec print-method print-dup throw-if printf format load compile get-in update-in pr pr-on newline ' +
      'flush read slurp read-line subvec with-open memfn time re-find re-groups rand-int rand mod locking ' +
      'assert-valid-fdecl alias resolve ref deref refset swap! reset! set-validator! compare-and-set! alter-meta! ' +
      'reset-meta! commute get-validator alter ref-set ref-history-count ref-min-history ref-max-history ensure sync io! ' +
      'new next conj set! to-array future future-call into-array aset gen-class reduce map filter find empty ' +
      'hash-map hash-set sorted-map sorted-map-by sorted-set sorted-set-by vec vector seq flatten reverse assoc dissoc list ' +
      'disj get union difference intersection extend extend-type extend-protocol int nth delay count concat chunk chunk-buffer ' +
      'chunk-append chunk-first chunk-rest max min dec unchecked-inc-int unchecked-inc unchecked-dec-inc unchecked-dec unchecked-negate ' +
      'unchecked-add-int unchecked-add unchecked-subtract-int unchecked-subtract chunk-next chunk-cons chunked-seq? prn vary-meta ' +
      'lazy-seq spread list* str find-keyword keyword symbol gensym force rationalize'
  };

  const SIMPLE_NUMBER_RE = '[-+]?\\d+(\\.\\d+)?';

  const SYMBOL = {
    begin: SYMBOL_RE,
    relevance: 0
  };
  const NUMBER = {
    className: 'number',
    begin: SIMPLE_NUMBER_RE,
    relevance: 0
  };
  const STRING = hljs.inherit(hljs.QUOTE_STRING_MODE, {
    illegal: null
  });
  const COMMENT = hljs.COMMENT(
    ';',
    '$',
    {
      relevance: 0
    }
  );
  const LITERAL = {
    className: 'literal',
    begin: /\b(true|false|nil)\b/
  };
  const COLLECTION = {
    begin: '[\\[\\{]',
    end: '[\\]\\}]'
  };
  const HINT = {
    className: 'comment',
    begin: '\\^' + SYMBOL_RE
  };
  const HINT_COL = hljs.COMMENT('\\^\\{', '\\}');
  const KEY = {
    className: 'symbol',
    begin: '[:]{1,2}' + SYMBOL_RE
  };
  const LIST = {
    begin: '\\(',
    end: '\\)'
  };
  const BODY = {
    endsWithParent: true,
    relevance: 0
  };
  const NAME = {
    keywords: keywords,
    className: 'name',
    begin: SYMBOL_RE,
    relevance: 0,
    starts: BODY
  };
  const DEFAULT_CONTAINS = [
    LIST,
    STRING,
    HINT,
    HINT_COL,
    COMMENT,
    KEY,
    COLLECTION,
    NUMBER,
    LITERAL,
    SYMBOL
  ];

  const GLOBAL = {
    beginKeywords: globals,
    lexemes: SYMBOL_RE,
    end: '(\\[|#|\\d|"|:|\\{|\\)|\\(|$)',
    contains: [
      {
        className: 'title',
        begin: SYMBOL_RE,
        relevance: 0,
        excludeEnd: true,
        // we can only have a single title
        endsParent: true
      }
    ].concat(DEFAULT_CONTAINS)
  };

  LIST.contains = [
    hljs.COMMENT('comment', ''),
    GLOBAL,
    NAME,
    BODY
  ];
  BODY.contains = DEFAULT_CONTAINS;
  COLLECTION.contains = DEFAULT_CONTAINS;
  HINT_COL.contains = [ COLLECTION ];

  return {
    name: 'Clojure',
    aliases: [ 'clj' ],
    illegal: /\S/,
    contains: [
      LIST,
      STRING,
      HINT,
      HINT_COL,
      COMMENT,
      KEY,
      COLLECTION,
      NUMBER,
      LITERAL
    ]
  };
}

module.exports = clojure;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY2xvanVyZS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxtRUFBbUU7QUFDbkU7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBLE1BQU07QUFDTjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG1CQUFtQjtBQUNuQixpQkFBaUI7QUFDakI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHVDQUF1QyxPQUFPO0FBQzlDO0FBQ0E7QUFDQSxnQkFBZ0IsSUFBSTtBQUNwQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSw0QkFBNEI7QUFDNUI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvY2xvanVyZS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IENsb2p1cmVcbkRlc2NyaXB0aW9uOiBDbG9qdXJlIHN5bnRheCAoYmFzZWQgb24gbGlzcC5qcylcbkF1dGhvcjogbWZvcm5vc1xuV2Vic2l0ZTogaHR0cHM6Ly9jbG9qdXJlLm9yZ1xuQ2F0ZWdvcnk6IGxpc3BcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBjbG9qdXJlKGhsanMpIHtcbiAgY29uc3QgU1lNQk9MU1RBUlQgPSAnYS16QS1aX1xcXFwtIS4/Kyo9PD4mI1xcJyc7XG4gIGNvbnN0IFNZTUJPTF9SRSA9ICdbJyArIFNZTUJPTFNUQVJUICsgJ11bJyArIFNZTUJPTFNUQVJUICsgJzAtOS87Ol0qJztcbiAgY29uc3QgZ2xvYmFscyA9ICdkZWYgZGVmb25jZSBkZWZwcm90b2NvbCBkZWZzdHJ1Y3QgZGVmbXVsdGkgZGVmbWV0aG9kIGRlZm4tIGRlZm4gZGVmbWFjcm8gZGVmdHlwZSBkZWZyZWNvcmQnO1xuICBjb25zdCBrZXl3b3JkcyA9IHtcbiAgICAkcGF0dGVybjogU1lNQk9MX1JFLFxuICAgICdidWlsdGluLW5hbWUnOlxuICAgICAgLy8gQ2xvanVyZSBrZXl3b3Jkc1xuICAgICAgZ2xvYmFscyArICcgJyArXG4gICAgICAnY29uZCBhcHBseSBpZi1ub3QgaWYtbGV0IGlmIG5vdCBub3Q9ID18MCA8fDAgPnwwIDw9fDAgPj18MCA9PXwwICt8MCAvfDAgKnwwIC18MCByZW0gJyArXG4gICAgICAncXVvdCBuZWc/IHBvcz8gZGVsYXk/IHN5bWJvbD8ga2V5d29yZD8gdHJ1ZT8gZmFsc2U/IGludGVnZXI/IGVtcHR5PyBjb2xsPyBsaXN0PyAnICtcbiAgICAgICdzZXQ/IGlmbj8gZm4/IGFzc29jaWF0aXZlPyBzZXF1ZW50aWFsPyBzb3J0ZWQ/IGNvdW50ZWQ/IHJldmVyc2libGU/IG51bWJlcj8gZGVjaW1hbD8gJyArXG4gICAgICAnY2xhc3M/IGRpc3RpbmN0PyBpc2E/IGZsb2F0PyByYXRpb25hbD8gcmVkdWNlZD8gcmF0aW8/IG9kZD8gZXZlbj8gY2hhcj8gc2VxPyB2ZWN0b3I/ICcgK1xuICAgICAgJ3N0cmluZz8gbWFwPyBuaWw/IGNvbnRhaW5zPyB6ZXJvPyBpbnN0YW5jZT8gbm90LWV2ZXJ5PyBub3QtYW55PyBsaWJzcGVjPyAtPiAtPj4gLi4gLiAnICtcbiAgICAgICdpbmMgY29tcGFyZSBkbyBkb3RpbWVzIG1hcGNhdCB0YWtlIHJlbW92ZSB0YWtlLXdoaWxlIGRyb3AgbGV0Zm4gZHJvcC1sYXN0IHRha2UtbGFzdCAnICtcbiAgICAgICdkcm9wLXdoaWxlIHdoaWxlIGludGVybiBjb25kcCBjYXNlIHJlZHVjZWQgY3ljbGUgc3BsaXQtYXQgc3BsaXQtd2l0aCByZXBlYXQgcmVwbGljYXRlICcgK1xuICAgICAgJ2l0ZXJhdGUgcmFuZ2UgbWVyZ2UgemlwbWFwIGRlY2xhcmUgbGluZS1zZXEgc29ydCBjb21wYXJhdG9yIHNvcnQtYnkgZG9ydW4gZG9hbGwgbnRobmV4dCAnICtcbiAgICAgICdudGhyZXN0IHBhcnRpdGlvbiBldmFsIGRvc2VxIGF3YWl0IGF3YWl0LWZvciBsZXQgYWdlbnQgYXRvbSBzZW5kIHNlbmQtb2ZmIHJlbGVhc2UtcGVuZGluZy1zZW5kcyAnICtcbiAgICAgICdhZGQtd2F0Y2ggbWFwdiBmaWx0ZXJ2IHJlbW92ZS13YXRjaCBhZ2VudC1lcnJvciByZXN0YXJ0LWFnZW50IHNldC1lcnJvci1oYW5kbGVyIGVycm9yLWhhbmRsZXIgJyArXG4gICAgICAnc2V0LWVycm9yLW1vZGUhIGVycm9yLW1vZGUgc2h1dGRvd24tYWdlbnRzIHF1b3RlIHZhciBmbiBsb29wIHJlY3VyIHRocm93IHRyeSBtb25pdG9yLWVudGVyICcgK1xuICAgICAgJ21vbml0b3ItZXhpdCBtYWNyb2V4cGFuZCBtYWNyb2V4cGFuZC0xIGZvciBkb3N5bmMgYW5kIG9yICcgK1xuICAgICAgJ3doZW4gd2hlbi1ub3Qgd2hlbi1sZXQgY29tcCBqdXh0IHBhcnRpYWwgc2VxdWVuY2UgbWVtb2l6ZSBjb25zdGFudGx5IGNvbXBsZW1lbnQgaWRlbnRpdHkgYXNzZXJ0ICcgK1xuICAgICAgJ3BlZWsgcG9wIGRvdG8gcHJveHkgZmlyc3QgcmVzdCBjb25zIGNhc3QgY29sbCBsYXN0IGJ1dGxhc3QgJyArXG4gICAgICAnc2lncyByZWlmeSBzZWNvbmQgZmZpcnN0IGZuZXh0IG5maXJzdCBubmV4dCBtZXRhIHdpdGgtbWV0YSBucyBpbi1ucyBjcmVhdGUtbnMgaW1wb3J0ICcgK1xuICAgICAgJ3JlZmVyIGtleXMgc2VsZWN0LWtleXMgdmFscyBrZXkgdmFsIHJzZXEgbmFtZSBuYW1lc3BhY2UgcHJvbWlzZSBpbnRvIHRyYW5zaWVudCBwZXJzaXN0ZW50ISBjb25qISAnICtcbiAgICAgICdhc3NvYyEgZGlzc29jISBwb3AhIGRpc2ohIHVzZSBjbGFzcyB0eXBlIG51bSBmbG9hdCBkb3VibGUgc2hvcnQgYnl0ZSBib29sZWFuIGJpZ2ludCBiaWdpbnRlZ2VyICcgK1xuICAgICAgJ2JpZ2RlYyBwcmludC1tZXRob2QgcHJpbnQtZHVwIHRocm93LWlmIHByaW50ZiBmb3JtYXQgbG9hZCBjb21waWxlIGdldC1pbiB1cGRhdGUtaW4gcHIgcHItb24gbmV3bGluZSAnICtcbiAgICAgICdmbHVzaCByZWFkIHNsdXJwIHJlYWQtbGluZSBzdWJ2ZWMgd2l0aC1vcGVuIG1lbWZuIHRpbWUgcmUtZmluZCByZS1ncm91cHMgcmFuZC1pbnQgcmFuZCBtb2QgbG9ja2luZyAnICtcbiAgICAgICdhc3NlcnQtdmFsaWQtZmRlY2wgYWxpYXMgcmVzb2x2ZSByZWYgZGVyZWYgcmVmc2V0IHN3YXAhIHJlc2V0ISBzZXQtdmFsaWRhdG9yISBjb21wYXJlLWFuZC1zZXQhIGFsdGVyLW1ldGEhICcgK1xuICAgICAgJ3Jlc2V0LW1ldGEhIGNvbW11dGUgZ2V0LXZhbGlkYXRvciBhbHRlciByZWYtc2V0IHJlZi1oaXN0b3J5LWNvdW50IHJlZi1taW4taGlzdG9yeSByZWYtbWF4LWhpc3RvcnkgZW5zdXJlIHN5bmMgaW8hICcgK1xuICAgICAgJ25ldyBuZXh0IGNvbmogc2V0ISB0by1hcnJheSBmdXR1cmUgZnV0dXJlLWNhbGwgaW50by1hcnJheSBhc2V0IGdlbi1jbGFzcyByZWR1Y2UgbWFwIGZpbHRlciBmaW5kIGVtcHR5ICcgK1xuICAgICAgJ2hhc2gtbWFwIGhhc2gtc2V0IHNvcnRlZC1tYXAgc29ydGVkLW1hcC1ieSBzb3J0ZWQtc2V0IHNvcnRlZC1zZXQtYnkgdmVjIHZlY3RvciBzZXEgZmxhdHRlbiByZXZlcnNlIGFzc29jIGRpc3NvYyBsaXN0ICcgK1xuICAgICAgJ2Rpc2ogZ2V0IHVuaW9uIGRpZmZlcmVuY2UgaW50ZXJzZWN0aW9uIGV4dGVuZCBleHRlbmQtdHlwZSBleHRlbmQtcHJvdG9jb2wgaW50IG50aCBkZWxheSBjb3VudCBjb25jYXQgY2h1bmsgY2h1bmstYnVmZmVyICcgK1xuICAgICAgJ2NodW5rLWFwcGVuZCBjaHVuay1maXJzdCBjaHVuay1yZXN0IG1heCBtaW4gZGVjIHVuY2hlY2tlZC1pbmMtaW50IHVuY2hlY2tlZC1pbmMgdW5jaGVja2VkLWRlYy1pbmMgdW5jaGVja2VkLWRlYyB1bmNoZWNrZWQtbmVnYXRlICcgK1xuICAgICAgJ3VuY2hlY2tlZC1hZGQtaW50IHVuY2hlY2tlZC1hZGQgdW5jaGVja2VkLXN1YnRyYWN0LWludCB1bmNoZWNrZWQtc3VidHJhY3QgY2h1bmstbmV4dCBjaHVuay1jb25zIGNodW5rZWQtc2VxPyBwcm4gdmFyeS1tZXRhICcgK1xuICAgICAgJ2xhenktc2VxIHNwcmVhZCBsaXN0KiBzdHIgZmluZC1rZXl3b3JkIGtleXdvcmQgc3ltYm9sIGdlbnN5bSBmb3JjZSByYXRpb25hbGl6ZSdcbiAgfTtcblxuICBjb25zdCBTSU1QTEVfTlVNQkVSX1JFID0gJ1stK10/XFxcXGQrKFxcXFwuXFxcXGQrKT8nO1xuXG4gIGNvbnN0IFNZTUJPTCA9IHtcbiAgICBiZWdpbjogU1lNQk9MX1JFLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICBjb25zdCBOVU1CRVIgPSB7XG4gICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICBiZWdpbjogU0lNUExFX05VTUJFUl9SRSxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgY29uc3QgU1RSSU5HID0gaGxqcy5pbmhlcml0KGhsanMuUVVPVEVfU1RSSU5HX01PREUsIHtcbiAgICBpbGxlZ2FsOiBudWxsXG4gIH0pO1xuICBjb25zdCBDT01NRU5UID0gaGxqcy5DT01NRU5UKFxuICAgICc7JyxcbiAgICAnJCcsXG4gICAge1xuICAgICAgcmVsZXZhbmNlOiAwXG4gICAgfVxuICApO1xuICBjb25zdCBMSVRFUkFMID0ge1xuICAgIGNsYXNzTmFtZTogJ2xpdGVyYWwnLFxuICAgIGJlZ2luOiAvXFxiKHRydWV8ZmFsc2V8bmlsKVxcYi9cbiAgfTtcbiAgY29uc3QgQ09MTEVDVElPTiA9IHtcbiAgICBiZWdpbjogJ1tcXFxcW1xcXFx7XScsXG4gICAgZW5kOiAnW1xcXFxdXFxcXH1dJ1xuICB9O1xuICBjb25zdCBISU5UID0ge1xuICAgIGNsYXNzTmFtZTogJ2NvbW1lbnQnLFxuICAgIGJlZ2luOiAnXFxcXF4nICsgU1lNQk9MX1JFXG4gIH07XG4gIGNvbnN0IEhJTlRfQ09MID0gaGxqcy5DT01NRU5UKCdcXFxcXlxcXFx7JywgJ1xcXFx9Jyk7XG4gIGNvbnN0IEtFWSA9IHtcbiAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgIGJlZ2luOiAnWzpdezEsMn0nICsgU1lNQk9MX1JFXG4gIH07XG4gIGNvbnN0IExJU1QgPSB7XG4gICAgYmVnaW46ICdcXFxcKCcsXG4gICAgZW5kOiAnXFxcXCknXG4gIH07XG4gIGNvbnN0IEJPRFkgPSB7XG4gICAgZW5kc1dpdGhQYXJlbnQ6IHRydWUsXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG4gIGNvbnN0IE5BTUUgPSB7XG4gICAga2V5d29yZHM6IGtleXdvcmRzLFxuICAgIGNsYXNzTmFtZTogJ25hbWUnLFxuICAgIGJlZ2luOiBTWU1CT0xfUkUsXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIHN0YXJ0czogQk9EWVxuICB9O1xuICBjb25zdCBERUZBVUxUX0NPTlRBSU5TID0gW1xuICAgIExJU1QsXG4gICAgU1RSSU5HLFxuICAgIEhJTlQsXG4gICAgSElOVF9DT0wsXG4gICAgQ09NTUVOVCxcbiAgICBLRVksXG4gICAgQ09MTEVDVElPTixcbiAgICBOVU1CRVIsXG4gICAgTElURVJBTCxcbiAgICBTWU1CT0xcbiAgXTtcblxuICBjb25zdCBHTE9CQUwgPSB7XG4gICAgYmVnaW5LZXl3b3JkczogZ2xvYmFscyxcbiAgICBsZXhlbWVzOiBTWU1CT0xfUkUsXG4gICAgZW5kOiAnKFxcXFxbfCN8XFxcXGR8XCJ8OnxcXFxce3xcXFxcKXxcXFxcKHwkKScsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndGl0bGUnLFxuICAgICAgICBiZWdpbjogU1lNQk9MX1JFLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIC8vIHdlIGNhbiBvbmx5IGhhdmUgYSBzaW5nbGUgdGl0bGVcbiAgICAgICAgZW5kc1BhcmVudDogdHJ1ZVxuICAgICAgfVxuICAgIF0uY29uY2F0KERFRkFVTFRfQ09OVEFJTlMpXG4gIH07XG5cbiAgTElTVC5jb250YWlucyA9IFtcbiAgICBobGpzLkNPTU1FTlQoJ2NvbW1lbnQnLCAnJyksXG4gICAgR0xPQkFMLFxuICAgIE5BTUUsXG4gICAgQk9EWVxuICBdO1xuICBCT0RZLmNvbnRhaW5zID0gREVGQVVMVF9DT05UQUlOUztcbiAgQ09MTEVDVElPTi5jb250YWlucyA9IERFRkFVTFRfQ09OVEFJTlM7XG4gIEhJTlRfQ09MLmNvbnRhaW5zID0gWyBDT0xMRUNUSU9OIF07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnQ2xvanVyZScsXG4gICAgYWxpYXNlczogWyAnY2xqJyBdLFxuICAgIGlsbGVnYWw6IC9cXFMvLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBMSVNULFxuICAgICAgU1RSSU5HLFxuICAgICAgSElOVCxcbiAgICAgIEhJTlRfQ09MLFxuICAgICAgQ09NTUVOVCxcbiAgICAgIEtFWSxcbiAgICAgIENPTExFQ1RJT04sXG4gICAgICBOVU1CRVIsXG4gICAgICBMSVRFUkFMXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGNsb2p1cmU7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=