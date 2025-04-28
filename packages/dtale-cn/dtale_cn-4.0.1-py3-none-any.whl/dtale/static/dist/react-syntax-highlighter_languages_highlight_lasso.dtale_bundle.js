(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_lasso"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/lasso.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/lasso.js ***!
  \************************************************************************************************/
/***/ ((module) => {

/*
Language: Lasso
Author: Eric Knibbe <eric@lassosoft.com>
Description: Lasso is a language and server platform for database-driven web applications. This definition handles Lasso 9 syntax and LassoScript for Lasso 8.6 and earlier.
Website: http://www.lassosoft.com/What-Is-Lasso
*/

function lasso(hljs) {
  const LASSO_IDENT_RE = '[a-zA-Z_][\\w.]*';
  const LASSO_ANGLE_RE = '<\\?(lasso(script)?|=)';
  const LASSO_CLOSE_RE = '\\]|\\?>';
  const LASSO_KEYWORDS = {
    $pattern: LASSO_IDENT_RE + '|&[lg]t;',
    literal:
      'true false none minimal full all void and or not ' +
      'bw nbw ew new cn ncn lt lte gt gte eq neq rx nrx ft',
    built_in:
      'array date decimal duration integer map pair string tag xml null ' +
      'boolean bytes keyword list locale queue set stack staticarray ' +
      'local var variable global data self inherited currentcapture givenblock',
    keyword:
      'cache database_names database_schemanames database_tablenames ' +
      'define_tag define_type email_batch encode_set html_comment handle ' +
      'handle_error header if inline iterate ljax_target link ' +
      'link_currentaction link_currentgroup link_currentrecord link_detail ' +
      'link_firstgroup link_firstrecord link_lastgroup link_lastrecord ' +
      'link_nextgroup link_nextrecord link_prevgroup link_prevrecord log ' +
      'loop namespace_using output_none portal private protect records ' +
      'referer referrer repeating resultset rows search_args ' +
      'search_arguments select sort_args sort_arguments thread_atomic ' +
      'value_list while abort case else fail_if fail_ifnot fail if_empty ' +
      'if_false if_null if_true loop_abort loop_continue loop_count params ' +
      'params_up return return_value run_children soap_definetag ' +
      'soap_lastrequest soap_lastresponse tag_name ascending average by ' +
      'define descending do equals frozen group handle_failure import in ' +
      'into join let match max min on order parent protected provide public ' +
      'require returnhome skip split_thread sum take thread to trait type ' +
      'where with yield yieldhome'
  };
  const HTML_COMMENT = hljs.COMMENT(
    '<!--',
    '-->',
    {
      relevance: 0
    }
  );
  const LASSO_NOPROCESS = {
    className: 'meta',
    begin: '\\[noprocess\\]',
    starts: {
      end: '\\[/noprocess\\]',
      returnEnd: true,
      contains: [HTML_COMMENT]
    }
  };
  const LASSO_START = {
    className: 'meta',
    begin: '\\[/noprocess|' + LASSO_ANGLE_RE
  };
  const LASSO_DATAMEMBER = {
    className: 'symbol',
    begin: '\'' + LASSO_IDENT_RE + '\''
  };
  const LASSO_CODE = [
    hljs.C_LINE_COMMENT_MODE,
    hljs.C_BLOCK_COMMENT_MODE,
    hljs.inherit(hljs.C_NUMBER_MODE, {
      begin: hljs.C_NUMBER_RE + '|(-?infinity|NaN)\\b'
    }),
    hljs.inherit(hljs.APOS_STRING_MODE, {
      illegal: null
    }),
    hljs.inherit(hljs.QUOTE_STRING_MODE, {
      illegal: null
    }),
    {
      className: 'string',
      begin: '`',
      end: '`'
    },
    { // variables
      variants: [
        {
          begin: '[#$]' + LASSO_IDENT_RE
        },
        {
          begin: '#',
          end: '\\d+',
          illegal: '\\W'
        }
      ]
    },
    {
      className: 'type',
      begin: '::\\s*',
      end: LASSO_IDENT_RE,
      illegal: '\\W'
    },
    {
      className: 'params',
      variants: [
        {
          begin: '-(?!infinity)' + LASSO_IDENT_RE,
          relevance: 0
        },
        {
          begin: '(\\.\\.\\.)'
        }
      ]
    },
    {
      begin: /(->|\.)\s*/,
      relevance: 0,
      contains: [LASSO_DATAMEMBER]
    },
    {
      className: 'class',
      beginKeywords: 'define',
      returnEnd: true,
      end: '\\(|=>',
      contains: [
        hljs.inherit(hljs.TITLE_MODE, {
          begin: LASSO_IDENT_RE + '(=(?!>))?|[-+*/%](?!>)'
        })
      ]
    }
  ];
  return {
    name: 'Lasso',
    aliases: [
      'ls',
      'lassoscript'
    ],
    case_insensitive: true,
    keywords: LASSO_KEYWORDS,
    contains: [
      {
        className: 'meta',
        begin: LASSO_CLOSE_RE,
        relevance: 0,
        starts: { // markup
          end: '\\[|' + LASSO_ANGLE_RE,
          returnEnd: true,
          relevance: 0,
          contains: [HTML_COMMENT]
        }
      },
      LASSO_NOPROCESS,
      LASSO_START,
      {
        className: 'meta',
        begin: '\\[no_square_brackets',
        starts: {
          end: '\\[/no_square_brackets\\]', // not implemented in the language
          keywords: LASSO_KEYWORDS,
          contains: [
            {
              className: 'meta',
              begin: LASSO_CLOSE_RE,
              relevance: 0,
              starts: {
                end: '\\[noprocess\\]|' + LASSO_ANGLE_RE,
                returnEnd: true,
                contains: [HTML_COMMENT]
              }
            },
            LASSO_NOPROCESS,
            LASSO_START
          ].concat(LASSO_CODE)
        }
      },
      {
        className: 'meta',
        begin: '\\[',
        relevance: 0
      },
      {
        className: 'meta',
        begin: '^#!',
        end: 'lasso9$',
        relevance: 10
      }
    ].concat(LASSO_CODE)
  };
}

module.exports = lasso;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbGFzc28uZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSx3Q0FBd0M7QUFDeEM7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMLE1BQU07QUFDTjtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxrQkFBa0I7QUFDbEI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9sYXNzby5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IExhc3NvXG5BdXRob3I6IEVyaWMgS25pYmJlIDxlcmljQGxhc3Nvc29mdC5jb20+XG5EZXNjcmlwdGlvbjogTGFzc28gaXMgYSBsYW5ndWFnZSBhbmQgc2VydmVyIHBsYXRmb3JtIGZvciBkYXRhYmFzZS1kcml2ZW4gd2ViIGFwcGxpY2F0aW9ucy4gVGhpcyBkZWZpbml0aW9uIGhhbmRsZXMgTGFzc28gOSBzeW50YXggYW5kIExhc3NvU2NyaXB0IGZvciBMYXNzbyA4LjYgYW5kIGVhcmxpZXIuXG5XZWJzaXRlOiBodHRwOi8vd3d3Lmxhc3Nvc29mdC5jb20vV2hhdC1Jcy1MYXNzb1xuKi9cblxuZnVuY3Rpb24gbGFzc28oaGxqcykge1xuICBjb25zdCBMQVNTT19JREVOVF9SRSA9ICdbYS16QS1aX11bXFxcXHcuXSonO1xuICBjb25zdCBMQVNTT19BTkdMRV9SRSA9ICc8XFxcXD8obGFzc28oc2NyaXB0KT98PSknO1xuICBjb25zdCBMQVNTT19DTE9TRV9SRSA9ICdcXFxcXXxcXFxcPz4nO1xuICBjb25zdCBMQVNTT19LRVlXT1JEUyA9IHtcbiAgICAkcGF0dGVybjogTEFTU09fSURFTlRfUkUgKyAnfCZbbGdddDsnLFxuICAgIGxpdGVyYWw6XG4gICAgICAndHJ1ZSBmYWxzZSBub25lIG1pbmltYWwgZnVsbCBhbGwgdm9pZCBhbmQgb3Igbm90ICcgK1xuICAgICAgJ2J3IG5idyBldyBuZXcgY24gbmNuIGx0IGx0ZSBndCBndGUgZXEgbmVxIHJ4IG5yeCBmdCcsXG4gICAgYnVpbHRfaW46XG4gICAgICAnYXJyYXkgZGF0ZSBkZWNpbWFsIGR1cmF0aW9uIGludGVnZXIgbWFwIHBhaXIgc3RyaW5nIHRhZyB4bWwgbnVsbCAnICtcbiAgICAgICdib29sZWFuIGJ5dGVzIGtleXdvcmQgbGlzdCBsb2NhbGUgcXVldWUgc2V0IHN0YWNrIHN0YXRpY2FycmF5ICcgK1xuICAgICAgJ2xvY2FsIHZhciB2YXJpYWJsZSBnbG9iYWwgZGF0YSBzZWxmIGluaGVyaXRlZCBjdXJyZW50Y2FwdHVyZSBnaXZlbmJsb2NrJyxcbiAgICBrZXl3b3JkOlxuICAgICAgJ2NhY2hlIGRhdGFiYXNlX25hbWVzIGRhdGFiYXNlX3NjaGVtYW5hbWVzIGRhdGFiYXNlX3RhYmxlbmFtZXMgJyArXG4gICAgICAnZGVmaW5lX3RhZyBkZWZpbmVfdHlwZSBlbWFpbF9iYXRjaCBlbmNvZGVfc2V0IGh0bWxfY29tbWVudCBoYW5kbGUgJyArXG4gICAgICAnaGFuZGxlX2Vycm9yIGhlYWRlciBpZiBpbmxpbmUgaXRlcmF0ZSBsamF4X3RhcmdldCBsaW5rICcgK1xuICAgICAgJ2xpbmtfY3VycmVudGFjdGlvbiBsaW5rX2N1cnJlbnRncm91cCBsaW5rX2N1cnJlbnRyZWNvcmQgbGlua19kZXRhaWwgJyArXG4gICAgICAnbGlua19maXJzdGdyb3VwIGxpbmtfZmlyc3RyZWNvcmQgbGlua19sYXN0Z3JvdXAgbGlua19sYXN0cmVjb3JkICcgK1xuICAgICAgJ2xpbmtfbmV4dGdyb3VwIGxpbmtfbmV4dHJlY29yZCBsaW5rX3ByZXZncm91cCBsaW5rX3ByZXZyZWNvcmQgbG9nICcgK1xuICAgICAgJ2xvb3AgbmFtZXNwYWNlX3VzaW5nIG91dHB1dF9ub25lIHBvcnRhbCBwcml2YXRlIHByb3RlY3QgcmVjb3JkcyAnICtcbiAgICAgICdyZWZlcmVyIHJlZmVycmVyIHJlcGVhdGluZyByZXN1bHRzZXQgcm93cyBzZWFyY2hfYXJncyAnICtcbiAgICAgICdzZWFyY2hfYXJndW1lbnRzIHNlbGVjdCBzb3J0X2FyZ3Mgc29ydF9hcmd1bWVudHMgdGhyZWFkX2F0b21pYyAnICtcbiAgICAgICd2YWx1ZV9saXN0IHdoaWxlIGFib3J0IGNhc2UgZWxzZSBmYWlsX2lmIGZhaWxfaWZub3QgZmFpbCBpZl9lbXB0eSAnICtcbiAgICAgICdpZl9mYWxzZSBpZl9udWxsIGlmX3RydWUgbG9vcF9hYm9ydCBsb29wX2NvbnRpbnVlIGxvb3BfY291bnQgcGFyYW1zICcgK1xuICAgICAgJ3BhcmFtc191cCByZXR1cm4gcmV0dXJuX3ZhbHVlIHJ1bl9jaGlsZHJlbiBzb2FwX2RlZmluZXRhZyAnICtcbiAgICAgICdzb2FwX2xhc3RyZXF1ZXN0IHNvYXBfbGFzdHJlc3BvbnNlIHRhZ19uYW1lIGFzY2VuZGluZyBhdmVyYWdlIGJ5ICcgK1xuICAgICAgJ2RlZmluZSBkZXNjZW5kaW5nIGRvIGVxdWFscyBmcm96ZW4gZ3JvdXAgaGFuZGxlX2ZhaWx1cmUgaW1wb3J0IGluICcgK1xuICAgICAgJ2ludG8gam9pbiBsZXQgbWF0Y2ggbWF4IG1pbiBvbiBvcmRlciBwYXJlbnQgcHJvdGVjdGVkIHByb3ZpZGUgcHVibGljICcgK1xuICAgICAgJ3JlcXVpcmUgcmV0dXJuaG9tZSBza2lwIHNwbGl0X3RocmVhZCBzdW0gdGFrZSB0aHJlYWQgdG8gdHJhaXQgdHlwZSAnICtcbiAgICAgICd3aGVyZSB3aXRoIHlpZWxkIHlpZWxkaG9tZSdcbiAgfTtcbiAgY29uc3QgSFRNTF9DT01NRU5UID0gaGxqcy5DT01NRU5UKFxuICAgICc8IS0tJyxcbiAgICAnLS0+JyxcbiAgICB7XG4gICAgICByZWxldmFuY2U6IDBcbiAgICB9XG4gICk7XG4gIGNvbnN0IExBU1NPX05PUFJPQ0VTUyA9IHtcbiAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICBiZWdpbjogJ1xcXFxbbm9wcm9jZXNzXFxcXF0nLFxuICAgIHN0YXJ0czoge1xuICAgICAgZW5kOiAnXFxcXFsvbm9wcm9jZXNzXFxcXF0nLFxuICAgICAgcmV0dXJuRW5kOiB0cnVlLFxuICAgICAgY29udGFpbnM6IFtIVE1MX0NPTU1FTlRdXG4gICAgfVxuICB9O1xuICBjb25zdCBMQVNTT19TVEFSVCA9IHtcbiAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICBiZWdpbjogJ1xcXFxbL25vcHJvY2Vzc3wnICsgTEFTU09fQU5HTEVfUkVcbiAgfTtcbiAgY29uc3QgTEFTU09fREFUQU1FTUJFUiA9IHtcbiAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgIGJlZ2luOiAnXFwnJyArIExBU1NPX0lERU5UX1JFICsgJ1xcJydcbiAgfTtcbiAgY29uc3QgTEFTU09fQ09ERSA9IFtcbiAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICBobGpzLmluaGVyaXQoaGxqcy5DX05VTUJFUl9NT0RFLCB7XG4gICAgICBiZWdpbjogaGxqcy5DX05VTUJFUl9SRSArICd8KC0/aW5maW5pdHl8TmFOKVxcXFxiJ1xuICAgIH0pLFxuICAgIGhsanMuaW5oZXJpdChobGpzLkFQT1NfU1RSSU5HX01PREUsIHtcbiAgICAgIGlsbGVnYWw6IG51bGxcbiAgICB9KSxcbiAgICBobGpzLmluaGVyaXQoaGxqcy5RVU9URV9TVFJJTkdfTU9ERSwge1xuICAgICAgaWxsZWdhbDogbnVsbFxuICAgIH0pLFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICBiZWdpbjogJ2AnLFxuICAgICAgZW5kOiAnYCdcbiAgICB9LFxuICAgIHsgLy8gdmFyaWFibGVzXG4gICAgICB2YXJpYW50czogW1xuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46ICdbIyRdJyArIExBU1NPX0lERU5UX1JFXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogJyMnLFxuICAgICAgICAgIGVuZDogJ1xcXFxkKycsXG4gICAgICAgICAgaWxsZWdhbDogJ1xcXFxXJ1xuICAgICAgICB9XG4gICAgICBdXG4gICAgfSxcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICd0eXBlJyxcbiAgICAgIGJlZ2luOiAnOjpcXFxccyonLFxuICAgICAgZW5kOiBMQVNTT19JREVOVF9SRSxcbiAgICAgIGlsbGVnYWw6ICdcXFxcVydcbiAgICB9LFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICB2YXJpYW50czogW1xuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46ICctKD8haW5maW5pdHkpJyArIExBU1NPX0lERU5UX1JFLFxuICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46ICcoXFxcXC5cXFxcLlxcXFwuKSdcbiAgICAgICAgfVxuICAgICAgXVxuICAgIH0sXG4gICAge1xuICAgICAgYmVnaW46IC8oLT58XFwuKVxccyovLFxuICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgY29udGFpbnM6IFtMQVNTT19EQVRBTUVNQkVSXVxuICAgIH0sXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgYmVnaW5LZXl3b3JkczogJ2RlZmluZScsXG4gICAgICByZXR1cm5FbmQ6IHRydWUsXG4gICAgICBlbmQ6ICdcXFxcKHw9PicsXG4gICAgICBjb250YWluczogW1xuICAgICAgICBobGpzLmluaGVyaXQoaGxqcy5USVRMRV9NT0RFLCB7XG4gICAgICAgICAgYmVnaW46IExBU1NPX0lERU5UX1JFICsgJyg9KD8hPikpP3xbLSsqLyVdKD8hPiknXG4gICAgICAgIH0pXG4gICAgICBdXG4gICAgfVxuICBdO1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdMYXNzbycsXG4gICAgYWxpYXNlczogW1xuICAgICAgJ2xzJyxcbiAgICAgICdsYXNzb3NjcmlwdCdcbiAgICBdLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAga2V5d29yZHM6IExBU1NPX0tFWVdPUkRTLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogTEFTU09fQ0xPU0VfUkUsXG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgc3RhcnRzOiB7IC8vIG1hcmt1cFxuICAgICAgICAgIGVuZDogJ1xcXFxbfCcgKyBMQVNTT19BTkdMRV9SRSxcbiAgICAgICAgICByZXR1cm5FbmQ6IHRydWUsXG4gICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgIGNvbnRhaW5zOiBbSFRNTF9DT01NRU5UXVxuICAgICAgICB9XG4gICAgICB9LFxuICAgICAgTEFTU09fTk9QUk9DRVNTLFxuICAgICAgTEFTU09fU1RBUlQsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogJ1xcXFxbbm9fc3F1YXJlX2JyYWNrZXRzJyxcbiAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgZW5kOiAnXFxcXFsvbm9fc3F1YXJlX2JyYWNrZXRzXFxcXF0nLCAvLyBub3QgaW1wbGVtZW50ZWQgaW4gdGhlIGxhbmd1YWdlXG4gICAgICAgICAga2V5d29yZHM6IExBU1NPX0tFWVdPUkRTLFxuICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICAgICAgICBiZWdpbjogTEFTU09fQ0xPU0VfUkUsXG4gICAgICAgICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgICAgICAgZW5kOiAnXFxcXFtub3Byb2Nlc3NcXFxcXXwnICsgTEFTU09fQU5HTEVfUkUsXG4gICAgICAgICAgICAgICAgcmV0dXJuRW5kOiB0cnVlLFxuICAgICAgICAgICAgICAgIGNvbnRhaW5zOiBbSFRNTF9DT01NRU5UXVxuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9LFxuICAgICAgICAgICAgTEFTU09fTk9QUk9DRVNTLFxuICAgICAgICAgICAgTEFTU09fU1RBUlRcbiAgICAgICAgICBdLmNvbmNhdChMQVNTT19DT0RFKVxuICAgICAgICB9XG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgYmVnaW46ICdcXFxcWycsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiAnXiMhJyxcbiAgICAgICAgZW5kOiAnbGFzc285JCcsXG4gICAgICAgIHJlbGV2YW5jZTogMTBcbiAgICAgIH1cbiAgICBdLmNvbmNhdChMQVNTT19DT0RFKVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGxhc3NvO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9