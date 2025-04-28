(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_fortran"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/fortran.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/fortran.js ***!
  \**************************************************************************************************/
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

/*
Language: Fortran
Author: Anthony Scemama <scemama@irsamc.ups-tlse.fr>
Website: https://en.wikipedia.org/wiki/Fortran
Category: scientific
*/

/** @type LanguageFn */
function fortran(hljs) {
  const PARAMS = {
    className: 'params',
    begin: '\\(',
    end: '\\)'
  };

  const COMMENT = {
    variants: [
      hljs.COMMENT('!', '$', {
        relevance: 0
      }),
      // allow FORTRAN 77 style comments
      hljs.COMMENT('^C[ ]', '$', {
        relevance: 0
      }),
      hljs.COMMENT('^C$', '$', {
        relevance: 0
      })
    ]
  };

  // regex in both fortran and irpf90 should match
  const OPTIONAL_NUMBER_SUFFIX = /(_[a-z_\d]+)?/;
  const OPTIONAL_NUMBER_EXP = /([de][+-]?\d+)?/;
  const NUMBER = {
    className: 'number',
    variants: [
      {
        begin: concat(/\b\d+/, /\.(\d*)/, OPTIONAL_NUMBER_EXP, OPTIONAL_NUMBER_SUFFIX)
      },
      {
        begin: concat(/\b\d+/, OPTIONAL_NUMBER_EXP, OPTIONAL_NUMBER_SUFFIX)
      },
      {
        begin: concat(/\.\d+/, OPTIONAL_NUMBER_EXP, OPTIONAL_NUMBER_SUFFIX)
      }
    ],
    relevance: 0
  };

  const FUNCTION_DEF = {
    className: 'function',
    beginKeywords: 'subroutine function program',
    illegal: '[${=\\n]',
    contains: [
      hljs.UNDERSCORE_TITLE_MODE,
      PARAMS
    ]
  };

  const STRING = {
    className: 'string',
    relevance: 0,
    variants: [
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE
    ]
  };

  const KEYWORDS = {
    literal: '.False. .True.',
    keyword: 'kind do concurrent local shared while private call intrinsic where elsewhere ' +
      'type endtype endmodule endselect endinterface end enddo endif if forall endforall only contains default return stop then block endblock endassociate ' +
      'public subroutine|10 function program .and. .or. .not. .le. .eq. .ge. .gt. .lt. ' +
      'goto save else use module select case ' +
      'access blank direct exist file fmt form formatted iostat name named nextrec number opened rec recl sequential status unformatted unit ' +
      'continue format pause cycle exit ' +
      'c_null_char c_alert c_backspace c_form_feed flush wait decimal round iomsg ' +
      'synchronous nopass non_overridable pass protected volatile abstract extends import ' +
      'non_intrinsic value deferred generic final enumerator class associate bind enum ' +
      'c_int c_short c_long c_long_long c_signed_char c_size_t c_int8_t c_int16_t c_int32_t c_int64_t c_int_least8_t c_int_least16_t ' +
      'c_int_least32_t c_int_least64_t c_int_fast8_t c_int_fast16_t c_int_fast32_t c_int_fast64_t c_intmax_t C_intptr_t c_float c_double ' +
      'c_long_double c_float_complex c_double_complex c_long_double_complex c_bool c_char c_null_ptr c_null_funptr ' +
      'c_new_line c_carriage_return c_horizontal_tab c_vertical_tab iso_c_binding c_loc c_funloc c_associated  c_f_pointer ' +
      'c_ptr c_funptr iso_fortran_env character_storage_size error_unit file_storage_size input_unit iostat_end iostat_eor ' +
      'numeric_storage_size output_unit c_f_procpointer ieee_arithmetic ieee_support_underflow_control ' +
      'ieee_get_underflow_mode ieee_set_underflow_mode newunit contiguous recursive ' +
      'pad position action delim readwrite eor advance nml interface procedure namelist include sequence elemental pure impure ' +
      'integer real character complex logical codimension dimension allocatable|10 parameter ' +
      'external implicit|10 none double precision assign intent optional pointer ' +
      'target in out common equivalence data',
    built_in: 'alog alog10 amax0 amax1 amin0 amin1 amod cabs ccos cexp clog csin csqrt dabs dacos dasin datan datan2 dcos dcosh ddim dexp dint ' +
      'dlog dlog10 dmax1 dmin1 dmod dnint dsign dsin dsinh dsqrt dtan dtanh float iabs idim idint idnint ifix isign max0 max1 min0 min1 sngl ' +
      'algama cdabs cdcos cdexp cdlog cdsin cdsqrt cqabs cqcos cqexp cqlog cqsin cqsqrt dcmplx dconjg derf derfc dfloat dgamma dimag dlgama ' +
      'iqint qabs qacos qasin qatan qatan2 qcmplx qconjg qcos qcosh qdim qerf qerfc qexp qgamma qimag qlgama qlog qlog10 qmax1 qmin1 qmod ' +
      'qnint qsign qsin qsinh qsqrt qtan qtanh abs acos aimag aint anint asin atan atan2 char cmplx conjg cos cosh exp ichar index int log ' +
      'log10 max min nint sign sin sinh sqrt tan tanh print write dim lge lgt lle llt mod nullify allocate deallocate ' +
      'adjustl adjustr all allocated any associated bit_size btest ceiling count cshift date_and_time digits dot_product ' +
      'eoshift epsilon exponent floor fraction huge iand ibclr ibits ibset ieor ior ishft ishftc lbound len_trim matmul ' +
      'maxexponent maxloc maxval merge minexponent minloc minval modulo mvbits nearest pack present product ' +
      'radix random_number random_seed range repeat reshape rrspacing scale scan selected_int_kind selected_real_kind ' +
      'set_exponent shape size spacing spread sum system_clock tiny transpose trim ubound unpack verify achar iachar transfer ' +
      'dble entry dprod cpu_time command_argument_count get_command get_command_argument get_environment_variable is_iostat_end ' +
      'ieee_arithmetic ieee_support_underflow_control ieee_get_underflow_mode ieee_set_underflow_mode ' +
      'is_iostat_eor move_alloc new_line selected_char_kind same_type_as extends_type_of ' +
      'acosh asinh atanh bessel_j0 bessel_j1 bessel_jn bessel_y0 bessel_y1 bessel_yn erf erfc erfc_scaled gamma log_gamma hypot norm2 ' +
      'atomic_define atomic_ref execute_command_line leadz trailz storage_size merge_bits ' +
      'bge bgt ble blt dshiftl dshiftr findloc iall iany iparity image_index lcobound ucobound maskl maskr ' +
      'num_images parity popcnt poppar shifta shiftl shiftr this_image sync change team co_broadcast co_max co_min co_sum co_reduce'
  };
  return {
    name: 'Fortran',
    case_insensitive: true,
    aliases: [
      'f90',
      'f95'
    ],
    keywords: KEYWORDS,
    illegal: /\/\*/,
    contains: [
      STRING,
      FUNCTION_DEF,
      // allow `C = value` for assignments so they aren't misdetected
      // as Fortran 77 style comments
      {
        begin: /^C\s*=(?!=)/,
        relevance: 0
      },
      COMMENT,
      NUMBER
    ]
  };
}

module.exports = fortran;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZm9ydHJhbi5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBLFdBQVcsUUFBUTtBQUNuQixhQUFhO0FBQ2I7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBLFdBQVcsdUJBQXVCO0FBQ2xDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9mb3J0cmFuLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogQHBhcmFtIHtzdHJpbmd9IHZhbHVlXG4gKiBAcmV0dXJucyB7UmVnRXhwfVxuICogKi9cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBzb3VyY2UocmUpIHtcbiAgaWYgKCFyZSkgcmV0dXJuIG51bGw7XG4gIGlmICh0eXBlb2YgcmUgPT09IFwic3RyaW5nXCIpIHJldHVybiByZTtcblxuICByZXR1cm4gcmUuc291cmNlO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7Li4uKFJlZ0V4cCB8IHN0cmluZykgfSBhcmdzXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBjb25jYXQoLi4uYXJncykge1xuICBjb25zdCBqb2luZWQgPSBhcmdzLm1hcCgoeCkgPT4gc291cmNlKHgpKS5qb2luKFwiXCIpO1xuICByZXR1cm4gam9pbmVkO1xufVxuXG4vKlxuTGFuZ3VhZ2U6IEZvcnRyYW5cbkF1dGhvcjogQW50aG9ueSBTY2VtYW1hIDxzY2VtYW1hQGlyc2FtYy51cHMtdGxzZS5mcj5cbldlYnNpdGU6IGh0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy93aWtpL0ZvcnRyYW5cbkNhdGVnb3J5OiBzY2llbnRpZmljXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gZm9ydHJhbihobGpzKSB7XG4gIGNvbnN0IFBBUkFNUyA9IHtcbiAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgIGJlZ2luOiAnXFxcXCgnLFxuICAgIGVuZDogJ1xcXFwpJ1xuICB9O1xuXG4gIGNvbnN0IENPTU1FTlQgPSB7XG4gICAgdmFyaWFudHM6IFtcbiAgICAgIGhsanMuQ09NTUVOVCgnIScsICckJywge1xuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0pLFxuICAgICAgLy8gYWxsb3cgRk9SVFJBTiA3NyBzdHlsZSBjb21tZW50c1xuICAgICAgaGxqcy5DT01NRU5UKCdeQ1sgXScsICckJywge1xuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0pLFxuICAgICAgaGxqcy5DT01NRU5UKCdeQyQnLCAnJCcsIHtcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9KVxuICAgIF1cbiAgfTtcblxuICAvLyByZWdleCBpbiBib3RoIGZvcnRyYW4gYW5kIGlycGY5MCBzaG91bGQgbWF0Y2hcbiAgY29uc3QgT1BUSU9OQUxfTlVNQkVSX1NVRkZJWCA9IC8oX1thLXpfXFxkXSspPy87XG4gIGNvbnN0IE9QVElPTkFMX05VTUJFUl9FWFAgPSAvKFtkZV1bKy1dP1xcZCspPy87XG4gIGNvbnN0IE5VTUJFUiA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBjb25jYXQoL1xcYlxcZCsvLCAvXFwuKFxcZCopLywgT1BUSU9OQUxfTlVNQkVSX0VYUCwgT1BUSU9OQUxfTlVNQkVSX1NVRkZJWClcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBjb25jYXQoL1xcYlxcZCsvLCBPUFRJT05BTF9OVU1CRVJfRVhQLCBPUFRJT05BTF9OVU1CRVJfU1VGRklYKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IGNvbmNhdCgvXFwuXFxkKy8sIE9QVElPTkFMX05VTUJFUl9FWFAsIE9QVElPTkFMX05VTUJFUl9TVUZGSVgpXG4gICAgICB9XG4gICAgXSxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcblxuICBjb25zdCBGVU5DVElPTl9ERUYgPSB7XG4gICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgIGJlZ2luS2V5d29yZHM6ICdzdWJyb3V0aW5lIGZ1bmN0aW9uIHByb2dyYW0nLFxuICAgIGlsbGVnYWw6ICdbJHs9XFxcXG5dJyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5VTkRFUlNDT1JFX1RJVExFX01PREUsXG4gICAgICBQQVJBTVNcbiAgICBdXG4gIH07XG5cbiAgY29uc3QgU1RSSU5HID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFXG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IEtFWVdPUkRTID0ge1xuICAgIGxpdGVyYWw6ICcuRmFsc2UuIC5UcnVlLicsXG4gICAga2V5d29yZDogJ2tpbmQgZG8gY29uY3VycmVudCBsb2NhbCBzaGFyZWQgd2hpbGUgcHJpdmF0ZSBjYWxsIGludHJpbnNpYyB3aGVyZSBlbHNld2hlcmUgJyArXG4gICAgICAndHlwZSBlbmR0eXBlIGVuZG1vZHVsZSBlbmRzZWxlY3QgZW5kaW50ZXJmYWNlIGVuZCBlbmRkbyBlbmRpZiBpZiBmb3JhbGwgZW5kZm9yYWxsIG9ubHkgY29udGFpbnMgZGVmYXVsdCByZXR1cm4gc3RvcCB0aGVuIGJsb2NrIGVuZGJsb2NrIGVuZGFzc29jaWF0ZSAnICtcbiAgICAgICdwdWJsaWMgc3Vicm91dGluZXwxMCBmdW5jdGlvbiBwcm9ncmFtIC5hbmQuIC5vci4gLm5vdC4gLmxlLiAuZXEuIC5nZS4gLmd0LiAubHQuICcgK1xuICAgICAgJ2dvdG8gc2F2ZSBlbHNlIHVzZSBtb2R1bGUgc2VsZWN0IGNhc2UgJyArXG4gICAgICAnYWNjZXNzIGJsYW5rIGRpcmVjdCBleGlzdCBmaWxlIGZtdCBmb3JtIGZvcm1hdHRlZCBpb3N0YXQgbmFtZSBuYW1lZCBuZXh0cmVjIG51bWJlciBvcGVuZWQgcmVjIHJlY2wgc2VxdWVudGlhbCBzdGF0dXMgdW5mb3JtYXR0ZWQgdW5pdCAnICtcbiAgICAgICdjb250aW51ZSBmb3JtYXQgcGF1c2UgY3ljbGUgZXhpdCAnICtcbiAgICAgICdjX251bGxfY2hhciBjX2FsZXJ0IGNfYmFja3NwYWNlIGNfZm9ybV9mZWVkIGZsdXNoIHdhaXQgZGVjaW1hbCByb3VuZCBpb21zZyAnICtcbiAgICAgICdzeW5jaHJvbm91cyBub3Bhc3Mgbm9uX292ZXJyaWRhYmxlIHBhc3MgcHJvdGVjdGVkIHZvbGF0aWxlIGFic3RyYWN0IGV4dGVuZHMgaW1wb3J0ICcgK1xuICAgICAgJ25vbl9pbnRyaW5zaWMgdmFsdWUgZGVmZXJyZWQgZ2VuZXJpYyBmaW5hbCBlbnVtZXJhdG9yIGNsYXNzIGFzc29jaWF0ZSBiaW5kIGVudW0gJyArXG4gICAgICAnY19pbnQgY19zaG9ydCBjX2xvbmcgY19sb25nX2xvbmcgY19zaWduZWRfY2hhciBjX3NpemVfdCBjX2ludDhfdCBjX2ludDE2X3QgY19pbnQzMl90IGNfaW50NjRfdCBjX2ludF9sZWFzdDhfdCBjX2ludF9sZWFzdDE2X3QgJyArXG4gICAgICAnY19pbnRfbGVhc3QzMl90IGNfaW50X2xlYXN0NjRfdCBjX2ludF9mYXN0OF90IGNfaW50X2Zhc3QxNl90IGNfaW50X2Zhc3QzMl90IGNfaW50X2Zhc3Q2NF90IGNfaW50bWF4X3QgQ19pbnRwdHJfdCBjX2Zsb2F0IGNfZG91YmxlICcgK1xuICAgICAgJ2NfbG9uZ19kb3VibGUgY19mbG9hdF9jb21wbGV4IGNfZG91YmxlX2NvbXBsZXggY19sb25nX2RvdWJsZV9jb21wbGV4IGNfYm9vbCBjX2NoYXIgY19udWxsX3B0ciBjX251bGxfZnVucHRyICcgK1xuICAgICAgJ2NfbmV3X2xpbmUgY19jYXJyaWFnZV9yZXR1cm4gY19ob3Jpem9udGFsX3RhYiBjX3ZlcnRpY2FsX3RhYiBpc29fY19iaW5kaW5nIGNfbG9jIGNfZnVubG9jIGNfYXNzb2NpYXRlZCAgY19mX3BvaW50ZXIgJyArXG4gICAgICAnY19wdHIgY19mdW5wdHIgaXNvX2ZvcnRyYW5fZW52IGNoYXJhY3Rlcl9zdG9yYWdlX3NpemUgZXJyb3JfdW5pdCBmaWxlX3N0b3JhZ2Vfc2l6ZSBpbnB1dF91bml0IGlvc3RhdF9lbmQgaW9zdGF0X2VvciAnICtcbiAgICAgICdudW1lcmljX3N0b3JhZ2Vfc2l6ZSBvdXRwdXRfdW5pdCBjX2ZfcHJvY3BvaW50ZXIgaWVlZV9hcml0aG1ldGljIGllZWVfc3VwcG9ydF91bmRlcmZsb3dfY29udHJvbCAnICtcbiAgICAgICdpZWVlX2dldF91bmRlcmZsb3dfbW9kZSBpZWVlX3NldF91bmRlcmZsb3dfbW9kZSBuZXd1bml0IGNvbnRpZ3VvdXMgcmVjdXJzaXZlICcgK1xuICAgICAgJ3BhZCBwb3NpdGlvbiBhY3Rpb24gZGVsaW0gcmVhZHdyaXRlIGVvciBhZHZhbmNlIG5tbCBpbnRlcmZhY2UgcHJvY2VkdXJlIG5hbWVsaXN0IGluY2x1ZGUgc2VxdWVuY2UgZWxlbWVudGFsIHB1cmUgaW1wdXJlICcgK1xuICAgICAgJ2ludGVnZXIgcmVhbCBjaGFyYWN0ZXIgY29tcGxleCBsb2dpY2FsIGNvZGltZW5zaW9uIGRpbWVuc2lvbiBhbGxvY2F0YWJsZXwxMCBwYXJhbWV0ZXIgJyArXG4gICAgICAnZXh0ZXJuYWwgaW1wbGljaXR8MTAgbm9uZSBkb3VibGUgcHJlY2lzaW9uIGFzc2lnbiBpbnRlbnQgb3B0aW9uYWwgcG9pbnRlciAnICtcbiAgICAgICd0YXJnZXQgaW4gb3V0IGNvbW1vbiBlcXVpdmFsZW5jZSBkYXRhJyxcbiAgICBidWlsdF9pbjogJ2Fsb2cgYWxvZzEwIGFtYXgwIGFtYXgxIGFtaW4wIGFtaW4xIGFtb2QgY2FicyBjY29zIGNleHAgY2xvZyBjc2luIGNzcXJ0IGRhYnMgZGFjb3MgZGFzaW4gZGF0YW4gZGF0YW4yIGRjb3MgZGNvc2ggZGRpbSBkZXhwIGRpbnQgJyArXG4gICAgICAnZGxvZyBkbG9nMTAgZG1heDEgZG1pbjEgZG1vZCBkbmludCBkc2lnbiBkc2luIGRzaW5oIGRzcXJ0IGR0YW4gZHRhbmggZmxvYXQgaWFicyBpZGltIGlkaW50IGlkbmludCBpZml4IGlzaWduIG1heDAgbWF4MSBtaW4wIG1pbjEgc25nbCAnICtcbiAgICAgICdhbGdhbWEgY2RhYnMgY2Rjb3MgY2RleHAgY2Rsb2cgY2RzaW4gY2RzcXJ0IGNxYWJzIGNxY29zIGNxZXhwIGNxbG9nIGNxc2luIGNxc3FydCBkY21wbHggZGNvbmpnIGRlcmYgZGVyZmMgZGZsb2F0IGRnYW1tYSBkaW1hZyBkbGdhbWEgJyArXG4gICAgICAnaXFpbnQgcWFicyBxYWNvcyBxYXNpbiBxYXRhbiBxYXRhbjIgcWNtcGx4IHFjb25qZyBxY29zIHFjb3NoIHFkaW0gcWVyZiBxZXJmYyBxZXhwIHFnYW1tYSBxaW1hZyBxbGdhbWEgcWxvZyBxbG9nMTAgcW1heDEgcW1pbjEgcW1vZCAnICtcbiAgICAgICdxbmludCBxc2lnbiBxc2luIHFzaW5oIHFzcXJ0IHF0YW4gcXRhbmggYWJzIGFjb3MgYWltYWcgYWludCBhbmludCBhc2luIGF0YW4gYXRhbjIgY2hhciBjbXBseCBjb25qZyBjb3MgY29zaCBleHAgaWNoYXIgaW5kZXggaW50IGxvZyAnICtcbiAgICAgICdsb2cxMCBtYXggbWluIG5pbnQgc2lnbiBzaW4gc2luaCBzcXJ0IHRhbiB0YW5oIHByaW50IHdyaXRlIGRpbSBsZ2UgbGd0IGxsZSBsbHQgbW9kIG51bGxpZnkgYWxsb2NhdGUgZGVhbGxvY2F0ZSAnICtcbiAgICAgICdhZGp1c3RsIGFkanVzdHIgYWxsIGFsbG9jYXRlZCBhbnkgYXNzb2NpYXRlZCBiaXRfc2l6ZSBidGVzdCBjZWlsaW5nIGNvdW50IGNzaGlmdCBkYXRlX2FuZF90aW1lIGRpZ2l0cyBkb3RfcHJvZHVjdCAnICtcbiAgICAgICdlb3NoaWZ0IGVwc2lsb24gZXhwb25lbnQgZmxvb3IgZnJhY3Rpb24gaHVnZSBpYW5kIGliY2xyIGliaXRzIGlic2V0IGllb3IgaW9yIGlzaGZ0IGlzaGZ0YyBsYm91bmQgbGVuX3RyaW0gbWF0bXVsICcgK1xuICAgICAgJ21heGV4cG9uZW50IG1heGxvYyBtYXh2YWwgbWVyZ2UgbWluZXhwb25lbnQgbWlubG9jIG1pbnZhbCBtb2R1bG8gbXZiaXRzIG5lYXJlc3QgcGFjayBwcmVzZW50IHByb2R1Y3QgJyArXG4gICAgICAncmFkaXggcmFuZG9tX251bWJlciByYW5kb21fc2VlZCByYW5nZSByZXBlYXQgcmVzaGFwZSBycnNwYWNpbmcgc2NhbGUgc2NhbiBzZWxlY3RlZF9pbnRfa2luZCBzZWxlY3RlZF9yZWFsX2tpbmQgJyArXG4gICAgICAnc2V0X2V4cG9uZW50IHNoYXBlIHNpemUgc3BhY2luZyBzcHJlYWQgc3VtIHN5c3RlbV9jbG9jayB0aW55IHRyYW5zcG9zZSB0cmltIHVib3VuZCB1bnBhY2sgdmVyaWZ5IGFjaGFyIGlhY2hhciB0cmFuc2ZlciAnICtcbiAgICAgICdkYmxlIGVudHJ5IGRwcm9kIGNwdV90aW1lIGNvbW1hbmRfYXJndW1lbnRfY291bnQgZ2V0X2NvbW1hbmQgZ2V0X2NvbW1hbmRfYXJndW1lbnQgZ2V0X2Vudmlyb25tZW50X3ZhcmlhYmxlIGlzX2lvc3RhdF9lbmQgJyArXG4gICAgICAnaWVlZV9hcml0aG1ldGljIGllZWVfc3VwcG9ydF91bmRlcmZsb3dfY29udHJvbCBpZWVlX2dldF91bmRlcmZsb3dfbW9kZSBpZWVlX3NldF91bmRlcmZsb3dfbW9kZSAnICtcbiAgICAgICdpc19pb3N0YXRfZW9yIG1vdmVfYWxsb2MgbmV3X2xpbmUgc2VsZWN0ZWRfY2hhcl9raW5kIHNhbWVfdHlwZV9hcyBleHRlbmRzX3R5cGVfb2YgJyArXG4gICAgICAnYWNvc2ggYXNpbmggYXRhbmggYmVzc2VsX2owIGJlc3NlbF9qMSBiZXNzZWxfam4gYmVzc2VsX3kwIGJlc3NlbF95MSBiZXNzZWxfeW4gZXJmIGVyZmMgZXJmY19zY2FsZWQgZ2FtbWEgbG9nX2dhbW1hIGh5cG90IG5vcm0yICcgK1xuICAgICAgJ2F0b21pY19kZWZpbmUgYXRvbWljX3JlZiBleGVjdXRlX2NvbW1hbmRfbGluZSBsZWFkeiB0cmFpbHogc3RvcmFnZV9zaXplIG1lcmdlX2JpdHMgJyArXG4gICAgICAnYmdlIGJndCBibGUgYmx0IGRzaGlmdGwgZHNoaWZ0ciBmaW5kbG9jIGlhbGwgaWFueSBpcGFyaXR5IGltYWdlX2luZGV4IGxjb2JvdW5kIHVjb2JvdW5kIG1hc2tsIG1hc2tyICcgK1xuICAgICAgJ251bV9pbWFnZXMgcGFyaXR5IHBvcGNudCBwb3BwYXIgc2hpZnRhIHNoaWZ0bCBzaGlmdHIgdGhpc19pbWFnZSBzeW5jIGNoYW5nZSB0ZWFtIGNvX2Jyb2FkY2FzdCBjb19tYXggY29fbWluIGNvX3N1bSBjb19yZWR1Y2UnXG4gIH07XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0ZvcnRyYW4nLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAgYWxpYXNlczogW1xuICAgICAgJ2Y5MCcsXG4gICAgICAnZjk1J1xuICAgIF0sXG4gICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgIGlsbGVnYWw6IC9cXC9cXCovLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBTVFJJTkcsXG4gICAgICBGVU5DVElPTl9ERUYsXG4gICAgICAvLyBhbGxvdyBgQyA9IHZhbHVlYCBmb3IgYXNzaWdubWVudHMgc28gdGhleSBhcmVuJ3QgbWlzZGV0ZWN0ZWRcbiAgICAgIC8vIGFzIEZvcnRyYW4gNzcgc3R5bGUgY29tbWVudHNcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9eQ1xccyo9KD8hPSkvLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICBDT01NRU5ULFxuICAgICAgTlVNQkVSXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGZvcnRyYW47XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=