(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_tp"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/tp.js":
/*!*********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/tp.js ***!
  \*********************************************************************************************/
/***/ ((module) => {

/*
Language: TP
Author: Jay Strybis <jay.strybis@gmail.com>
Description: FANUC TP programming language (TPP).
*/

function tp(hljs) {
  const TPID = {
    className: 'number',
    begin: '[1-9][0-9]*', /* no leading zeros */
    relevance: 0
  };
  const TPLABEL = {
    className: 'symbol',
    begin: ':[^\\]]+'
  };
  const TPDATA = {
    className: 'built_in',
    begin: '(AR|P|PAYLOAD|PR|R|SR|RSR|LBL|VR|UALM|MESSAGE|UTOOL|UFRAME|TIMER|' +
    'TIMER_OVERFLOW|JOINT_MAX_SPEED|RESUME_PROG|DIAG_REC)\\[',
    end: '\\]',
    contains: [
      'self',
      TPID,
      TPLABEL
    ]
  };
  const TPIO = {
    className: 'built_in',
    begin: '(AI|AO|DI|DO|F|RI|RO|UI|UO|GI|GO|SI|SO)\\[',
    end: '\\]',
    contains: [
      'self',
      TPID,
      hljs.QUOTE_STRING_MODE, /* for pos section at bottom */
      TPLABEL
    ]
  };

  return {
    name: 'TP',
    keywords: {
      keyword:
        'ABORT ACC ADJUST AND AP_LD BREAK CALL CNT COL CONDITION CONFIG DA DB ' +
        'DIV DETECT ELSE END ENDFOR ERR_NUM ERROR_PROG FINE FOR GP GUARD INC ' +
        'IF JMP LINEAR_MAX_SPEED LOCK MOD MONITOR OFFSET Offset OR OVERRIDE ' +
        'PAUSE PREG PTH RT_LD RUN SELECT SKIP Skip TA TB TO TOOL_OFFSET ' +
        'Tool_Offset UF UT UFRAME_NUM UTOOL_NUM UNLOCK WAIT X Y Z W P R STRLEN ' +
        'SUBSTR FINDSTR VOFFSET PROG ATTR MN POS',
      literal:
        'ON OFF max_speed LPOS JPOS ENABLE DISABLE START STOP RESET'
    },
    contains: [
      TPDATA,
      TPIO,
      {
        className: 'keyword',
        begin: '/(PROG|ATTR|MN|POS|END)\\b'
      },
      {
        /* this is for cases like ,CALL */
        className: 'keyword',
        begin: '(CALL|RUN|POINT_LOGIC|LBL)\\b'
      },
      {
        /* this is for cases like CNT100 where the default lexemes do not
         * separate the keyword and the number */
        className: 'keyword',
        begin: '\\b(ACC|CNT|Skip|Offset|PSPD|RT_LD|AP_LD|Tool_Offset)'
      },
      {
        /* to catch numbers that do not have a word boundary on the left */
        className: 'number',
        begin: '\\d+(sec|msec|mm/sec|cm/min|inch/min|deg/sec|mm|in|cm)?\\b',
        relevance: 0
      },
      hljs.COMMENT('//', '[;$]'),
      hljs.COMMENT('!', '[;$]'),
      hljs.COMMENT('--eg:', '$'),
      hljs.QUOTE_STRING_MODE,
      {
        className: 'string',
        begin: '\'',
        end: '\''
      },
      hljs.C_NUMBER_MODE,
      {
        className: 'variable',
        begin: '\\$[A-Za-z0-9_]+'
      }
    ]
  };
}

module.exports = tp;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfdHAuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQLDRCQUE0QjtBQUM1QiwyQkFBMkI7QUFDM0I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3RwLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogVFBcbkF1dGhvcjogSmF5IFN0cnliaXMgPGpheS5zdHJ5YmlzQGdtYWlsLmNvbT5cbkRlc2NyaXB0aW9uOiBGQU5VQyBUUCBwcm9ncmFtbWluZyBsYW5ndWFnZSAoVFBQKS5cbiovXG5cbmZ1bmN0aW9uIHRwKGhsanMpIHtcbiAgY29uc3QgVFBJRCA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIGJlZ2luOiAnWzEtOV1bMC05XSonLCAvKiBubyBsZWFkaW5nIHplcm9zICovXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG4gIGNvbnN0IFRQTEFCRUwgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICBiZWdpbjogJzpbXlxcXFxdXSsnXG4gIH07XG4gIGNvbnN0IFRQREFUQSA9IHtcbiAgICBjbGFzc05hbWU6ICdidWlsdF9pbicsXG4gICAgYmVnaW46ICcoQVJ8UHxQQVlMT0FEfFBSfFJ8U1J8UlNSfExCTHxWUnxVQUxNfE1FU1NBR0V8VVRPT0x8VUZSQU1FfFRJTUVSfCcgK1xuICAgICdUSU1FUl9PVkVSRkxPV3xKT0lOVF9NQVhfU1BFRUR8UkVTVU1FX1BST0d8RElBR19SRUMpXFxcXFsnLFxuICAgIGVuZDogJ1xcXFxdJyxcbiAgICBjb250YWluczogW1xuICAgICAgJ3NlbGYnLFxuICAgICAgVFBJRCxcbiAgICAgIFRQTEFCRUxcbiAgICBdXG4gIH07XG4gIGNvbnN0IFRQSU8gPSB7XG4gICAgY2xhc3NOYW1lOiAnYnVpbHRfaW4nLFxuICAgIGJlZ2luOiAnKEFJfEFPfERJfERPfEZ8Ukl8Uk98VUl8VU98R0l8R098U0l8U08pXFxcXFsnLFxuICAgIGVuZDogJ1xcXFxdJyxcbiAgICBjb250YWluczogW1xuICAgICAgJ3NlbGYnLFxuICAgICAgVFBJRCxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsIC8qIGZvciBwb3Mgc2VjdGlvbiBhdCBib3R0b20gKi9cbiAgICAgIFRQTEFCRUxcbiAgICBdXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnVFAnLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBrZXl3b3JkOlxuICAgICAgICAnQUJPUlQgQUNDIEFESlVTVCBBTkQgQVBfTEQgQlJFQUsgQ0FMTCBDTlQgQ09MIENPTkRJVElPTiBDT05GSUcgREEgREIgJyArXG4gICAgICAgICdESVYgREVURUNUIEVMU0UgRU5EIEVOREZPUiBFUlJfTlVNIEVSUk9SX1BST0cgRklORSBGT1IgR1AgR1VBUkQgSU5DICcgK1xuICAgICAgICAnSUYgSk1QIExJTkVBUl9NQVhfU1BFRUQgTE9DSyBNT0QgTU9OSVRPUiBPRkZTRVQgT2Zmc2V0IE9SIE9WRVJSSURFICcgK1xuICAgICAgICAnUEFVU0UgUFJFRyBQVEggUlRfTEQgUlVOIFNFTEVDVCBTS0lQIFNraXAgVEEgVEIgVE8gVE9PTF9PRkZTRVQgJyArXG4gICAgICAgICdUb29sX09mZnNldCBVRiBVVCBVRlJBTUVfTlVNIFVUT09MX05VTSBVTkxPQ0sgV0FJVCBYIFkgWiBXIFAgUiBTVFJMRU4gJyArXG4gICAgICAgICdTVUJTVFIgRklORFNUUiBWT0ZGU0VUIFBST0cgQVRUUiBNTiBQT1MnLFxuICAgICAgbGl0ZXJhbDpcbiAgICAgICAgJ09OIE9GRiBtYXhfc3BlZWQgTFBPUyBKUE9TIEVOQUJMRSBESVNBQkxFIFNUQVJUIFNUT1AgUkVTRVQnXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAgVFBEQVRBLFxuICAgICAgVFBJTyxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgICAgIGJlZ2luOiAnLyhQUk9HfEFUVFJ8TU58UE9TfEVORClcXFxcYidcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8qIHRoaXMgaXMgZm9yIGNhc2VzIGxpa2UgLENBTEwgKi9cbiAgICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgICAgIGJlZ2luOiAnKENBTEx8UlVOfFBPSU5UX0xPR0lDfExCTClcXFxcYidcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8qIHRoaXMgaXMgZm9yIGNhc2VzIGxpa2UgQ05UMTAwIHdoZXJlIHRoZSBkZWZhdWx0IGxleGVtZXMgZG8gbm90XG4gICAgICAgICAqIHNlcGFyYXRlIHRoZSBrZXl3b3JkIGFuZCB0aGUgbnVtYmVyICovXG4gICAgICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgICAgICBiZWdpbjogJ1xcXFxiKEFDQ3xDTlR8U2tpcHxPZmZzZXR8UFNQRHxSVF9MRHxBUF9MRHxUb29sX09mZnNldCknXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvKiB0byBjYXRjaCBudW1iZXJzIHRoYXQgZG8gbm90IGhhdmUgYSB3b3JkIGJvdW5kYXJ5IG9uIHRoZSBsZWZ0ICovXG4gICAgICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgICAgIGJlZ2luOiAnXFxcXGQrKHNlY3xtc2VjfG1tL3NlY3xjbS9taW58aW5jaC9taW58ZGVnL3NlY3xtbXxpbnxjbSk/XFxcXGInLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICBobGpzLkNPTU1FTlQoJy8vJywgJ1s7JF0nKSxcbiAgICAgIGhsanMuQ09NTUVOVCgnIScsICdbOyRdJyksXG4gICAgICBobGpzLkNPTU1FTlQoJy0tZWc6JywgJyQnKSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgIGJlZ2luOiAnXFwnJyxcbiAgICAgICAgZW5kOiAnXFwnJ1xuICAgICAgfSxcbiAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndmFyaWFibGUnLFxuICAgICAgICBiZWdpbjogJ1xcXFwkW0EtWmEtejAtOV9dKydcbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gdHA7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=