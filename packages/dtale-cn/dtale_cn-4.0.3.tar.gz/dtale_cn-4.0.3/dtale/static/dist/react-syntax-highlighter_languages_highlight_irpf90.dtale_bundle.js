(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_irpf90"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/irpf90.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/irpf90.js ***!
  \*************************************************************************************************/
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
Language: IRPF90
Author: Anthony Scemama <scemama@irsamc.ups-tlse.fr>
Description: IRPF90 is an open-source Fortran code generator
Website: http://irpf90.ups-tlse.fr
Category: scientific
*/

/** @type LanguageFn */
function irpf90(hljs) {
  const PARAMS = {
    className: 'params',
    begin: '\\(',
    end: '\\)'
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

  const F_KEYWORDS = {
    literal: '.False. .True.',
    keyword: 'kind do while private call intrinsic where elsewhere ' +
      'type endtype endmodule endselect endinterface end enddo endif if forall endforall only contains default return stop then ' +
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
      'pad position action delim readwrite eor advance nml interface procedure namelist include sequence elemental pure ' +
      'integer real character complex logical dimension allocatable|10 parameter ' +
      'external implicit|10 none double precision assign intent optional pointer ' +
      'target in out common equivalence data ' +
      // IRPF90 special keywords
      'begin_provider &begin_provider end_provider begin_shell end_shell begin_template end_template subst assert touch ' +
      'soft_touch provide no_dep free irp_if irp_else irp_endif irp_write irp_read',
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
      'num_images parity popcnt poppar shifta shiftl shiftr this_image ' +
      // IRPF90 special built_ins
      'IRP_ALIGN irp_here'
  };
  return {
    name: 'IRPF90',
    case_insensitive: true,
    keywords: F_KEYWORDS,
    illegal: /\/\*/,
    contains: [
      hljs.inherit(hljs.APOS_STRING_MODE, {
        className: 'string',
        relevance: 0
      }),
      hljs.inherit(hljs.QUOTE_STRING_MODE, {
        className: 'string',
        relevance: 0
      }),
      {
        className: 'function',
        beginKeywords: 'subroutine function program',
        illegal: '[${=\\n]',
        contains: [
          hljs.UNDERSCORE_TITLE_MODE,
          PARAMS
        ]
      },
      hljs.COMMENT('!', '$', {
        relevance: 0
      }),
      hljs.COMMENT('begin_doc', 'end_doc', {
        relevance: 10
      }),
      NUMBER
    ]
  };
}

module.exports = irpf90;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfaXJwZjkwLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0EsV0FBVyxRQUFRO0FBQ25CLGFBQWE7QUFDYjs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyx1QkFBdUI7QUFDbEMsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EscUJBQXFCO0FBQ3JCO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvaXJwZjkwLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogQHBhcmFtIHtzdHJpbmd9IHZhbHVlXG4gKiBAcmV0dXJucyB7UmVnRXhwfVxuICogKi9cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBzb3VyY2UocmUpIHtcbiAgaWYgKCFyZSkgcmV0dXJuIG51bGw7XG4gIGlmICh0eXBlb2YgcmUgPT09IFwic3RyaW5nXCIpIHJldHVybiByZTtcblxuICByZXR1cm4gcmUuc291cmNlO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7Li4uKFJlZ0V4cCB8IHN0cmluZykgfSBhcmdzXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBjb25jYXQoLi4uYXJncykge1xuICBjb25zdCBqb2luZWQgPSBhcmdzLm1hcCgoeCkgPT4gc291cmNlKHgpKS5qb2luKFwiXCIpO1xuICByZXR1cm4gam9pbmVkO1xufVxuXG4vKlxuTGFuZ3VhZ2U6IElSUEY5MFxuQXV0aG9yOiBBbnRob255IFNjZW1hbWEgPHNjZW1hbWFAaXJzYW1jLnVwcy10bHNlLmZyPlxuRGVzY3JpcHRpb246IElSUEY5MCBpcyBhbiBvcGVuLXNvdXJjZSBGb3J0cmFuIGNvZGUgZ2VuZXJhdG9yXG5XZWJzaXRlOiBodHRwOi8vaXJwZjkwLnVwcy10bHNlLmZyXG5DYXRlZ29yeTogc2NpZW50aWZpY1xuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGlycGY5MChobGpzKSB7XG4gIGNvbnN0IFBBUkFNUyA9IHtcbiAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgIGJlZ2luOiAnXFxcXCgnLFxuICAgIGVuZDogJ1xcXFwpJ1xuICB9O1xuXG4gIC8vIHJlZ2V4IGluIGJvdGggZm9ydHJhbiBhbmQgaXJwZjkwIHNob3VsZCBtYXRjaFxuICBjb25zdCBPUFRJT05BTF9OVU1CRVJfU1VGRklYID0gLyhfW2Etel9cXGRdKyk/LztcbiAgY29uc3QgT1BUSU9OQUxfTlVNQkVSX0VYUCA9IC8oW2RlXVsrLV0/XFxkKyk/LztcbiAgY29uc3QgTlVNQkVSID0ge1xuICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IGNvbmNhdCgvXFxiXFxkKy8sIC9cXC4oXFxkKikvLCBPUFRJT05BTF9OVU1CRVJfRVhQLCBPUFRJT05BTF9OVU1CRVJfU1VGRklYKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IGNvbmNhdCgvXFxiXFxkKy8sIE9QVElPTkFMX05VTUJFUl9FWFAsIE9QVElPTkFMX05VTUJFUl9TVUZGSVgpXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogY29uY2F0KC9cXC5cXGQrLywgT1BUSU9OQUxfTlVNQkVSX0VYUCwgT1BUSU9OQUxfTlVNQkVSX1NVRkZJWClcbiAgICAgIH1cbiAgICBdLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuXG4gIGNvbnN0IEZfS0VZV09SRFMgPSB7XG4gICAgbGl0ZXJhbDogJy5GYWxzZS4gLlRydWUuJyxcbiAgICBrZXl3b3JkOiAna2luZCBkbyB3aGlsZSBwcml2YXRlIGNhbGwgaW50cmluc2ljIHdoZXJlIGVsc2V3aGVyZSAnICtcbiAgICAgICd0eXBlIGVuZHR5cGUgZW5kbW9kdWxlIGVuZHNlbGVjdCBlbmRpbnRlcmZhY2UgZW5kIGVuZGRvIGVuZGlmIGlmIGZvcmFsbCBlbmRmb3JhbGwgb25seSBjb250YWlucyBkZWZhdWx0IHJldHVybiBzdG9wIHRoZW4gJyArXG4gICAgICAncHVibGljIHN1YnJvdXRpbmV8MTAgZnVuY3Rpb24gcHJvZ3JhbSAuYW5kLiAub3IuIC5ub3QuIC5sZS4gLmVxLiAuZ2UuIC5ndC4gLmx0LiAnICtcbiAgICAgICdnb3RvIHNhdmUgZWxzZSB1c2UgbW9kdWxlIHNlbGVjdCBjYXNlICcgK1xuICAgICAgJ2FjY2VzcyBibGFuayBkaXJlY3QgZXhpc3QgZmlsZSBmbXQgZm9ybSBmb3JtYXR0ZWQgaW9zdGF0IG5hbWUgbmFtZWQgbmV4dHJlYyBudW1iZXIgb3BlbmVkIHJlYyByZWNsIHNlcXVlbnRpYWwgc3RhdHVzIHVuZm9ybWF0dGVkIHVuaXQgJyArXG4gICAgICAnY29udGludWUgZm9ybWF0IHBhdXNlIGN5Y2xlIGV4aXQgJyArXG4gICAgICAnY19udWxsX2NoYXIgY19hbGVydCBjX2JhY2tzcGFjZSBjX2Zvcm1fZmVlZCBmbHVzaCB3YWl0IGRlY2ltYWwgcm91bmQgaW9tc2cgJyArXG4gICAgICAnc3luY2hyb25vdXMgbm9wYXNzIG5vbl9vdmVycmlkYWJsZSBwYXNzIHByb3RlY3RlZCB2b2xhdGlsZSBhYnN0cmFjdCBleHRlbmRzIGltcG9ydCAnICtcbiAgICAgICdub25faW50cmluc2ljIHZhbHVlIGRlZmVycmVkIGdlbmVyaWMgZmluYWwgZW51bWVyYXRvciBjbGFzcyBhc3NvY2lhdGUgYmluZCBlbnVtICcgK1xuICAgICAgJ2NfaW50IGNfc2hvcnQgY19sb25nIGNfbG9uZ19sb25nIGNfc2lnbmVkX2NoYXIgY19zaXplX3QgY19pbnQ4X3QgY19pbnQxNl90IGNfaW50MzJfdCBjX2ludDY0X3QgY19pbnRfbGVhc3Q4X3QgY19pbnRfbGVhc3QxNl90ICcgK1xuICAgICAgJ2NfaW50X2xlYXN0MzJfdCBjX2ludF9sZWFzdDY0X3QgY19pbnRfZmFzdDhfdCBjX2ludF9mYXN0MTZfdCBjX2ludF9mYXN0MzJfdCBjX2ludF9mYXN0NjRfdCBjX2ludG1heF90IENfaW50cHRyX3QgY19mbG9hdCBjX2RvdWJsZSAnICtcbiAgICAgICdjX2xvbmdfZG91YmxlIGNfZmxvYXRfY29tcGxleCBjX2RvdWJsZV9jb21wbGV4IGNfbG9uZ19kb3VibGVfY29tcGxleCBjX2Jvb2wgY19jaGFyIGNfbnVsbF9wdHIgY19udWxsX2Z1bnB0ciAnICtcbiAgICAgICdjX25ld19saW5lIGNfY2FycmlhZ2VfcmV0dXJuIGNfaG9yaXpvbnRhbF90YWIgY192ZXJ0aWNhbF90YWIgaXNvX2NfYmluZGluZyBjX2xvYyBjX2Z1bmxvYyBjX2Fzc29jaWF0ZWQgIGNfZl9wb2ludGVyICcgK1xuICAgICAgJ2NfcHRyIGNfZnVucHRyIGlzb19mb3J0cmFuX2VudiBjaGFyYWN0ZXJfc3RvcmFnZV9zaXplIGVycm9yX3VuaXQgZmlsZV9zdG9yYWdlX3NpemUgaW5wdXRfdW5pdCBpb3N0YXRfZW5kIGlvc3RhdF9lb3IgJyArXG4gICAgICAnbnVtZXJpY19zdG9yYWdlX3NpemUgb3V0cHV0X3VuaXQgY19mX3Byb2Nwb2ludGVyIGllZWVfYXJpdGhtZXRpYyBpZWVlX3N1cHBvcnRfdW5kZXJmbG93X2NvbnRyb2wgJyArXG4gICAgICAnaWVlZV9nZXRfdW5kZXJmbG93X21vZGUgaWVlZV9zZXRfdW5kZXJmbG93X21vZGUgbmV3dW5pdCBjb250aWd1b3VzIHJlY3Vyc2l2ZSAnICtcbiAgICAgICdwYWQgcG9zaXRpb24gYWN0aW9uIGRlbGltIHJlYWR3cml0ZSBlb3IgYWR2YW5jZSBubWwgaW50ZXJmYWNlIHByb2NlZHVyZSBuYW1lbGlzdCBpbmNsdWRlIHNlcXVlbmNlIGVsZW1lbnRhbCBwdXJlICcgK1xuICAgICAgJ2ludGVnZXIgcmVhbCBjaGFyYWN0ZXIgY29tcGxleCBsb2dpY2FsIGRpbWVuc2lvbiBhbGxvY2F0YWJsZXwxMCBwYXJhbWV0ZXIgJyArXG4gICAgICAnZXh0ZXJuYWwgaW1wbGljaXR8MTAgbm9uZSBkb3VibGUgcHJlY2lzaW9uIGFzc2lnbiBpbnRlbnQgb3B0aW9uYWwgcG9pbnRlciAnICtcbiAgICAgICd0YXJnZXQgaW4gb3V0IGNvbW1vbiBlcXVpdmFsZW5jZSBkYXRhICcgK1xuICAgICAgLy8gSVJQRjkwIHNwZWNpYWwga2V5d29yZHNcbiAgICAgICdiZWdpbl9wcm92aWRlciAmYmVnaW5fcHJvdmlkZXIgZW5kX3Byb3ZpZGVyIGJlZ2luX3NoZWxsIGVuZF9zaGVsbCBiZWdpbl90ZW1wbGF0ZSBlbmRfdGVtcGxhdGUgc3Vic3QgYXNzZXJ0IHRvdWNoICcgK1xuICAgICAgJ3NvZnRfdG91Y2ggcHJvdmlkZSBub19kZXAgZnJlZSBpcnBfaWYgaXJwX2Vsc2UgaXJwX2VuZGlmIGlycF93cml0ZSBpcnBfcmVhZCcsXG4gICAgYnVpbHRfaW46ICdhbG9nIGFsb2cxMCBhbWF4MCBhbWF4MSBhbWluMCBhbWluMSBhbW9kIGNhYnMgY2NvcyBjZXhwIGNsb2cgY3NpbiBjc3FydCBkYWJzIGRhY29zIGRhc2luIGRhdGFuIGRhdGFuMiBkY29zIGRjb3NoIGRkaW0gZGV4cCBkaW50ICcgK1xuICAgICAgJ2Rsb2cgZGxvZzEwIGRtYXgxIGRtaW4xIGRtb2QgZG5pbnQgZHNpZ24gZHNpbiBkc2luaCBkc3FydCBkdGFuIGR0YW5oIGZsb2F0IGlhYnMgaWRpbSBpZGludCBpZG5pbnQgaWZpeCBpc2lnbiBtYXgwIG1heDEgbWluMCBtaW4xIHNuZ2wgJyArXG4gICAgICAnYWxnYW1hIGNkYWJzIGNkY29zIGNkZXhwIGNkbG9nIGNkc2luIGNkc3FydCBjcWFicyBjcWNvcyBjcWV4cCBjcWxvZyBjcXNpbiBjcXNxcnQgZGNtcGx4IGRjb25qZyBkZXJmIGRlcmZjIGRmbG9hdCBkZ2FtbWEgZGltYWcgZGxnYW1hICcgK1xuICAgICAgJ2lxaW50IHFhYnMgcWFjb3MgcWFzaW4gcWF0YW4gcWF0YW4yIHFjbXBseCBxY29uamcgcWNvcyBxY29zaCBxZGltIHFlcmYgcWVyZmMgcWV4cCBxZ2FtbWEgcWltYWcgcWxnYW1hIHFsb2cgcWxvZzEwIHFtYXgxIHFtaW4xIHFtb2QgJyArXG4gICAgICAncW5pbnQgcXNpZ24gcXNpbiBxc2luaCBxc3FydCBxdGFuIHF0YW5oIGFicyBhY29zIGFpbWFnIGFpbnQgYW5pbnQgYXNpbiBhdGFuIGF0YW4yIGNoYXIgY21wbHggY29uamcgY29zIGNvc2ggZXhwIGljaGFyIGluZGV4IGludCBsb2cgJyArXG4gICAgICAnbG9nMTAgbWF4IG1pbiBuaW50IHNpZ24gc2luIHNpbmggc3FydCB0YW4gdGFuaCBwcmludCB3cml0ZSBkaW0gbGdlIGxndCBsbGUgbGx0IG1vZCBudWxsaWZ5IGFsbG9jYXRlIGRlYWxsb2NhdGUgJyArXG4gICAgICAnYWRqdXN0bCBhZGp1c3RyIGFsbCBhbGxvY2F0ZWQgYW55IGFzc29jaWF0ZWQgYml0X3NpemUgYnRlc3QgY2VpbGluZyBjb3VudCBjc2hpZnQgZGF0ZV9hbmRfdGltZSBkaWdpdHMgZG90X3Byb2R1Y3QgJyArXG4gICAgICAnZW9zaGlmdCBlcHNpbG9uIGV4cG9uZW50IGZsb29yIGZyYWN0aW9uIGh1Z2UgaWFuZCBpYmNsciBpYml0cyBpYnNldCBpZW9yIGlvciBpc2hmdCBpc2hmdGMgbGJvdW5kIGxlbl90cmltIG1hdG11bCAnICtcbiAgICAgICdtYXhleHBvbmVudCBtYXhsb2MgbWF4dmFsIG1lcmdlIG1pbmV4cG9uZW50IG1pbmxvYyBtaW52YWwgbW9kdWxvIG12Yml0cyBuZWFyZXN0IHBhY2sgcHJlc2VudCBwcm9kdWN0ICcgK1xuICAgICAgJ3JhZGl4IHJhbmRvbV9udW1iZXIgcmFuZG9tX3NlZWQgcmFuZ2UgcmVwZWF0IHJlc2hhcGUgcnJzcGFjaW5nIHNjYWxlIHNjYW4gc2VsZWN0ZWRfaW50X2tpbmQgc2VsZWN0ZWRfcmVhbF9raW5kICcgK1xuICAgICAgJ3NldF9leHBvbmVudCBzaGFwZSBzaXplIHNwYWNpbmcgc3ByZWFkIHN1bSBzeXN0ZW1fY2xvY2sgdGlueSB0cmFuc3Bvc2UgdHJpbSB1Ym91bmQgdW5wYWNrIHZlcmlmeSBhY2hhciBpYWNoYXIgdHJhbnNmZXIgJyArXG4gICAgICAnZGJsZSBlbnRyeSBkcHJvZCBjcHVfdGltZSBjb21tYW5kX2FyZ3VtZW50X2NvdW50IGdldF9jb21tYW5kIGdldF9jb21tYW5kX2FyZ3VtZW50IGdldF9lbnZpcm9ubWVudF92YXJpYWJsZSBpc19pb3N0YXRfZW5kICcgK1xuICAgICAgJ2llZWVfYXJpdGhtZXRpYyBpZWVlX3N1cHBvcnRfdW5kZXJmbG93X2NvbnRyb2wgaWVlZV9nZXRfdW5kZXJmbG93X21vZGUgaWVlZV9zZXRfdW5kZXJmbG93X21vZGUgJyArXG4gICAgICAnaXNfaW9zdGF0X2VvciBtb3ZlX2FsbG9jIG5ld19saW5lIHNlbGVjdGVkX2NoYXJfa2luZCBzYW1lX3R5cGVfYXMgZXh0ZW5kc190eXBlX29mICcgK1xuICAgICAgJ2Fjb3NoIGFzaW5oIGF0YW5oIGJlc3NlbF9qMCBiZXNzZWxfajEgYmVzc2VsX2puIGJlc3NlbF95MCBiZXNzZWxfeTEgYmVzc2VsX3luIGVyZiBlcmZjIGVyZmNfc2NhbGVkIGdhbW1hIGxvZ19nYW1tYSBoeXBvdCBub3JtMiAnICtcbiAgICAgICdhdG9taWNfZGVmaW5lIGF0b21pY19yZWYgZXhlY3V0ZV9jb21tYW5kX2xpbmUgbGVhZHogdHJhaWx6IHN0b3JhZ2Vfc2l6ZSBtZXJnZV9iaXRzICcgK1xuICAgICAgJ2JnZSBiZ3QgYmxlIGJsdCBkc2hpZnRsIGRzaGlmdHIgZmluZGxvYyBpYWxsIGlhbnkgaXBhcml0eSBpbWFnZV9pbmRleCBsY29ib3VuZCB1Y29ib3VuZCBtYXNrbCBtYXNrciAnICtcbiAgICAgICdudW1faW1hZ2VzIHBhcml0eSBwb3BjbnQgcG9wcGFyIHNoaWZ0YSBzaGlmdGwgc2hpZnRyIHRoaXNfaW1hZ2UgJyArXG4gICAgICAvLyBJUlBGOTAgc3BlY2lhbCBidWlsdF9pbnNcbiAgICAgICdJUlBfQUxJR04gaXJwX2hlcmUnXG4gIH07XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0lSUEY5MCcsXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBrZXl3b3JkczogRl9LRVlXT1JEUyxcbiAgICBpbGxlZ2FsOiAvXFwvXFwqLyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5pbmhlcml0KGhsanMuQVBPU19TVFJJTkdfTU9ERSwge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0pLFxuICAgICAgaGxqcy5pbmhlcml0KGhsanMuUVVPVEVfU1RSSU5HX01PREUsIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9KSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnc3Vicm91dGluZSBmdW5jdGlvbiBwcm9ncmFtJyxcbiAgICAgICAgaWxsZWdhbDogJ1skez1cXFxcbl0nLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuVU5ERVJTQ09SRV9USVRMRV9NT0RFLFxuICAgICAgICAgIFBBUkFNU1xuICAgICAgICBdXG4gICAgICB9LFxuICAgICAgaGxqcy5DT01NRU5UKCchJywgJyQnLCB7XG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSksXG4gICAgICBobGpzLkNPTU1FTlQoJ2JlZ2luX2RvYycsICdlbmRfZG9jJywge1xuICAgICAgICByZWxldmFuY2U6IDEwXG4gICAgICB9KSxcbiAgICAgIE5VTUJFUlxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBpcnBmOTA7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=