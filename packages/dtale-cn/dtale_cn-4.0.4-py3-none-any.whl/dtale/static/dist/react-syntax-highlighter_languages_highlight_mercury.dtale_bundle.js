(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_mercury"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/mercury.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/mercury.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
Language: Mercury
Author: mucaho <mkucko@gmail.com>
Description: Mercury is a logic/functional programming language which combines the clarity and expressiveness of declarative programming with advanced static analysis and error detection features.
Website: https://www.mercurylang.org
*/

function mercury(hljs) {
  const KEYWORDS = {
    keyword:
      'module use_module import_module include_module end_module initialise ' +
      'mutable initialize finalize finalise interface implementation pred ' +
      'mode func type inst solver any_pred any_func is semidet det nondet ' +
      'multi erroneous failure cc_nondet cc_multi typeclass instance where ' +
      'pragma promise external trace atomic or_else require_complete_switch ' +
      'require_det require_semidet require_multi require_nondet ' +
      'require_cc_multi require_cc_nondet require_erroneous require_failure',
    meta:
      // pragma
      'inline no_inline type_spec source_file fact_table obsolete memo ' +
      'loop_check minimal_model terminates does_not_terminate ' +
      'check_termination promise_equivalent_clauses ' +
      // preprocessor
      'foreign_proc foreign_decl foreign_code foreign_type ' +
      'foreign_import_module foreign_export_enum foreign_export ' +
      'foreign_enum may_call_mercury will_not_call_mercury thread_safe ' +
      'not_thread_safe maybe_thread_safe promise_pure promise_semipure ' +
      'tabled_for_io local untrailed trailed attach_to_io_state ' +
      'can_pass_as_mercury_type stable will_not_throw_exception ' +
      'may_modify_trail will_not_modify_trail may_duplicate ' +
      'may_not_duplicate affects_liveness does_not_affect_liveness ' +
      'doesnt_affect_liveness no_sharing unknown_sharing sharing',
    built_in:
      'some all not if then else true fail false try catch catch_any ' +
      'semidet_true semidet_false semidet_fail impure_true impure semipure'
  };

  const COMMENT = hljs.COMMENT('%', '$');

  const NUMCODE = {
    className: 'number',
    begin: "0'.\\|0[box][0-9a-fA-F]*"
  };

  const ATOM = hljs.inherit(hljs.APOS_STRING_MODE, {
    relevance: 0
  });
  const STRING = hljs.inherit(hljs.QUOTE_STRING_MODE, {
    relevance: 0
  });
  const STRING_FMT = {
    className: 'subst',
    begin: '\\\\[abfnrtv]\\|\\\\x[0-9a-fA-F]*\\\\\\|%[-+# *.0-9]*[dioxXucsfeEgGp]',
    relevance: 0
  };
  STRING.contains = STRING.contains.slice(); // we need our own copy of contains
  STRING.contains.push(STRING_FMT);

  const IMPLICATION = {
    className: 'built_in',
    variants: [
      {
        begin: '<=>'
      },
      {
        begin: '<=',
        relevance: 0
      },
      {
        begin: '=>',
        relevance: 0
      },
      {
        begin: '/\\\\'
      },
      {
        begin: '\\\\/'
      }
    ]
  };

  const HEAD_BODY_CONJUNCTION = {
    className: 'built_in',
    variants: [
      {
        begin: ':-\\|-->'
      },
      {
        begin: '=',
        relevance: 0
      }
    ]
  };

  return {
    name: 'Mercury',
    aliases: [
      'm',
      'moo'
    ],
    keywords: KEYWORDS,
    contains: [
      IMPLICATION,
      HEAD_BODY_CONJUNCTION,
      COMMENT,
      hljs.C_BLOCK_COMMENT_MODE,
      NUMCODE,
      hljs.NUMBER_MODE,
      ATOM,
      STRING,
      { // relevance booster
        begin: /:-/
      },
      { // relevance booster
        begin: /\.$/
      }
    ]
  };
}

module.exports = mercury;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbWVyY3VyeS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0EsR0FBRztBQUNIO0FBQ0E7QUFDQSxHQUFHO0FBQ0g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDZDQUE2QztBQUM3Qzs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsUUFBUTtBQUNSO0FBQ0EsT0FBTztBQUNQLFFBQVE7QUFDUjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9tZXJjdXJ5LmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogTWVyY3VyeVxuQXV0aG9yOiBtdWNhaG8gPG1rdWNrb0BnbWFpbC5jb20+XG5EZXNjcmlwdGlvbjogTWVyY3VyeSBpcyBhIGxvZ2ljL2Z1bmN0aW9uYWwgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2Ugd2hpY2ggY29tYmluZXMgdGhlIGNsYXJpdHkgYW5kIGV4cHJlc3NpdmVuZXNzIG9mIGRlY2xhcmF0aXZlIHByb2dyYW1taW5nIHdpdGggYWR2YW5jZWQgc3RhdGljIGFuYWx5c2lzIGFuZCBlcnJvciBkZXRlY3Rpb24gZmVhdHVyZXMuXG5XZWJzaXRlOiBodHRwczovL3d3dy5tZXJjdXJ5bGFuZy5vcmdcbiovXG5cbmZ1bmN0aW9uIG1lcmN1cnkoaGxqcykge1xuICBjb25zdCBLRVlXT1JEUyA9IHtcbiAgICBrZXl3b3JkOlxuICAgICAgJ21vZHVsZSB1c2VfbW9kdWxlIGltcG9ydF9tb2R1bGUgaW5jbHVkZV9tb2R1bGUgZW5kX21vZHVsZSBpbml0aWFsaXNlICcgK1xuICAgICAgJ211dGFibGUgaW5pdGlhbGl6ZSBmaW5hbGl6ZSBmaW5hbGlzZSBpbnRlcmZhY2UgaW1wbGVtZW50YXRpb24gcHJlZCAnICtcbiAgICAgICdtb2RlIGZ1bmMgdHlwZSBpbnN0IHNvbHZlciBhbnlfcHJlZCBhbnlfZnVuYyBpcyBzZW1pZGV0IGRldCBub25kZXQgJyArXG4gICAgICAnbXVsdGkgZXJyb25lb3VzIGZhaWx1cmUgY2Nfbm9uZGV0IGNjX211bHRpIHR5cGVjbGFzcyBpbnN0YW5jZSB3aGVyZSAnICtcbiAgICAgICdwcmFnbWEgcHJvbWlzZSBleHRlcm5hbCB0cmFjZSBhdG9taWMgb3JfZWxzZSByZXF1aXJlX2NvbXBsZXRlX3N3aXRjaCAnICtcbiAgICAgICdyZXF1aXJlX2RldCByZXF1aXJlX3NlbWlkZXQgcmVxdWlyZV9tdWx0aSByZXF1aXJlX25vbmRldCAnICtcbiAgICAgICdyZXF1aXJlX2NjX211bHRpIHJlcXVpcmVfY2Nfbm9uZGV0IHJlcXVpcmVfZXJyb25lb3VzIHJlcXVpcmVfZmFpbHVyZScsXG4gICAgbWV0YTpcbiAgICAgIC8vIHByYWdtYVxuICAgICAgJ2lubGluZSBub19pbmxpbmUgdHlwZV9zcGVjIHNvdXJjZV9maWxlIGZhY3RfdGFibGUgb2Jzb2xldGUgbWVtbyAnICtcbiAgICAgICdsb29wX2NoZWNrIG1pbmltYWxfbW9kZWwgdGVybWluYXRlcyBkb2VzX25vdF90ZXJtaW5hdGUgJyArXG4gICAgICAnY2hlY2tfdGVybWluYXRpb24gcHJvbWlzZV9lcXVpdmFsZW50X2NsYXVzZXMgJyArXG4gICAgICAvLyBwcmVwcm9jZXNzb3JcbiAgICAgICdmb3JlaWduX3Byb2MgZm9yZWlnbl9kZWNsIGZvcmVpZ25fY29kZSBmb3JlaWduX3R5cGUgJyArXG4gICAgICAnZm9yZWlnbl9pbXBvcnRfbW9kdWxlIGZvcmVpZ25fZXhwb3J0X2VudW0gZm9yZWlnbl9leHBvcnQgJyArXG4gICAgICAnZm9yZWlnbl9lbnVtIG1heV9jYWxsX21lcmN1cnkgd2lsbF9ub3RfY2FsbF9tZXJjdXJ5IHRocmVhZF9zYWZlICcgK1xuICAgICAgJ25vdF90aHJlYWRfc2FmZSBtYXliZV90aHJlYWRfc2FmZSBwcm9taXNlX3B1cmUgcHJvbWlzZV9zZW1pcHVyZSAnICtcbiAgICAgICd0YWJsZWRfZm9yX2lvIGxvY2FsIHVudHJhaWxlZCB0cmFpbGVkIGF0dGFjaF90b19pb19zdGF0ZSAnICtcbiAgICAgICdjYW5fcGFzc19hc19tZXJjdXJ5X3R5cGUgc3RhYmxlIHdpbGxfbm90X3Rocm93X2V4Y2VwdGlvbiAnICtcbiAgICAgICdtYXlfbW9kaWZ5X3RyYWlsIHdpbGxfbm90X21vZGlmeV90cmFpbCBtYXlfZHVwbGljYXRlICcgK1xuICAgICAgJ21heV9ub3RfZHVwbGljYXRlIGFmZmVjdHNfbGl2ZW5lc3MgZG9lc19ub3RfYWZmZWN0X2xpdmVuZXNzICcgK1xuICAgICAgJ2RvZXNudF9hZmZlY3RfbGl2ZW5lc3Mgbm9fc2hhcmluZyB1bmtub3duX3NoYXJpbmcgc2hhcmluZycsXG4gICAgYnVpbHRfaW46XG4gICAgICAnc29tZSBhbGwgbm90IGlmIHRoZW4gZWxzZSB0cnVlIGZhaWwgZmFsc2UgdHJ5IGNhdGNoIGNhdGNoX2FueSAnICtcbiAgICAgICdzZW1pZGV0X3RydWUgc2VtaWRldF9mYWxzZSBzZW1pZGV0X2ZhaWwgaW1wdXJlX3RydWUgaW1wdXJlIHNlbWlwdXJlJ1xuICB9O1xuXG4gIGNvbnN0IENPTU1FTlQgPSBobGpzLkNPTU1FTlQoJyUnLCAnJCcpO1xuXG4gIGNvbnN0IE5VTUNPREUgPSB7XG4gICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICBiZWdpbjogXCIwJy5cXFxcfDBbYm94XVswLTlhLWZBLUZdKlwiXG4gIH07XG5cbiAgY29uc3QgQVRPTSA9IGhsanMuaW5oZXJpdChobGpzLkFQT1NfU1RSSU5HX01PREUsIHtcbiAgICByZWxldmFuY2U6IDBcbiAgfSk7XG4gIGNvbnN0IFNUUklORyA9IGhsanMuaW5oZXJpdChobGpzLlFVT1RFX1NUUklOR19NT0RFLCB7XG4gICAgcmVsZXZhbmNlOiAwXG4gIH0pO1xuICBjb25zdCBTVFJJTkdfRk1UID0ge1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICBiZWdpbjogJ1xcXFxcXFxcW2FiZm5ydHZdXFxcXHxcXFxcXFxcXHhbMC05YS1mQS1GXSpcXFxcXFxcXFxcXFx8JVstKyMgKi4wLTldKltkaW94WHVjc2ZlRWdHcF0nLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICBTVFJJTkcuY29udGFpbnMgPSBTVFJJTkcuY29udGFpbnMuc2xpY2UoKTsgLy8gd2UgbmVlZCBvdXIgb3duIGNvcHkgb2YgY29udGFpbnNcbiAgU1RSSU5HLmNvbnRhaW5zLnB1c2goU1RSSU5HX0ZNVCk7XG5cbiAgY29uc3QgSU1QTElDQVRJT04gPSB7XG4gICAgY2xhc3NOYW1lOiAnYnVpbHRfaW4nLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnPD0+J1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICc8PScsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICc9PicsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICcvXFxcXFxcXFwnXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcXFxcXFxcLydcbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgY29uc3QgSEVBRF9CT0RZX0NPTkpVTkNUSU9OID0ge1xuICAgIGNsYXNzTmFtZTogJ2J1aWx0X2luJyxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogJzotXFxcXHwtLT4nXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJz0nLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnTWVyY3VyeScsXG4gICAgYWxpYXNlczogW1xuICAgICAgJ20nLFxuICAgICAgJ21vbydcbiAgICBdLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBjb250YWluczogW1xuICAgICAgSU1QTElDQVRJT04sXG4gICAgICBIRUFEX0JPRFlfQ09OSlVOQ1RJT04sXG4gICAgICBDT01NRU5ULFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIE5VTUNPREUsXG4gICAgICBobGpzLk5VTUJFUl9NT0RFLFxuICAgICAgQVRPTSxcbiAgICAgIFNUUklORyxcbiAgICAgIHsgLy8gcmVsZXZhbmNlIGJvb3N0ZXJcbiAgICAgICAgYmVnaW46IC86LS9cbiAgICAgIH0sXG4gICAgICB7IC8vIHJlbGV2YW5jZSBib29zdGVyXG4gICAgICAgIGJlZ2luOiAvXFwuJC9cbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gbWVyY3VyeTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==