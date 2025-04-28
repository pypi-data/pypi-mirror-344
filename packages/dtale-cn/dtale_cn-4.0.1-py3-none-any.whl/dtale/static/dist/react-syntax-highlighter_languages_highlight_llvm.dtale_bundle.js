(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_llvm"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/llvm.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/llvm.js ***!
  \***********************************************************************************************/
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
Language: LLVM IR
Author: Michael Rodler <contact@f0rki.at>
Description: language used as intermediate representation in the LLVM compiler framework
Website: https://llvm.org/docs/LangRef.html
Category: assembler
Audit: 2020
*/

/** @type LanguageFn */
function llvm(hljs) {
  const IDENT_RE = /([-a-zA-Z$._][\w$.-]*)/;
  const TYPE = {
    className: 'type',
    begin: /\bi\d+(?=\s|\b)/
  };
  const OPERATOR = {
    className: 'operator',
    relevance: 0,
    begin: /=/
  };
  const PUNCTUATION = {
    className: 'punctuation',
    relevance: 0,
    begin: /,/
  };
  const NUMBER = {
    className: 'number',
    variants: [
        { begin: /0[xX][a-fA-F0-9]+/ },
        { begin: /-?\d+(?:[.]\d+)?(?:[eE][-+]?\d+(?:[.]\d+)?)?/ }
    ],
    relevance: 0
  };
  const LABEL = {
    className: 'symbol',
    variants: [
        { begin: /^\s*[a-z]+:/ }, // labels
    ],
    relevance: 0
  };
  const VARIABLE = {
    className: 'variable',
    variants: [
      { begin: concat(/%/, IDENT_RE) },
      { begin: /%\d+/ },
      { begin: /#\d+/ },
    ]
  };
  const FUNCTION = {
    className: 'title',
    variants: [
      { begin: concat(/@/, IDENT_RE) },
      { begin: /@\d+/ },
      { begin: concat(/!/, IDENT_RE) },
      { begin: concat(/!\d+/, IDENT_RE) },
      // https://llvm.org/docs/LangRef.html#namedmetadatastructure
      // obviously a single digit can also be used in this fashion
      { begin: /!\d+/ }
    ]
  };

  return {
    name: 'LLVM IR',
    // TODO: split into different categories of keywords
    keywords:
      'begin end true false declare define global ' +
      'constant private linker_private internal ' +
      'available_externally linkonce linkonce_odr weak ' +
      'weak_odr appending dllimport dllexport common ' +
      'default hidden protected extern_weak external ' +
      'thread_local zeroinitializer undef null to tail ' +
      'target triple datalayout volatile nuw nsw nnan ' +
      'ninf nsz arcp fast exact inbounds align ' +
      'addrspace section alias module asm sideeffect ' +
      'gc dbg linker_private_weak attributes blockaddress ' +
      'initialexec localdynamic localexec prefix unnamed_addr ' +
      'ccc fastcc coldcc x86_stdcallcc x86_fastcallcc ' +
      'arm_apcscc arm_aapcscc arm_aapcs_vfpcc ptx_device ' +
      'ptx_kernel intel_ocl_bicc msp430_intrcc spir_func ' +
      'spir_kernel x86_64_sysvcc x86_64_win64cc x86_thiscallcc ' +
      'cc c signext zeroext inreg sret nounwind ' +
      'noreturn noalias nocapture byval nest readnone ' +
      'readonly inlinehint noinline alwaysinline optsize ssp ' +
      'sspreq noredzone noimplicitfloat naked builtin cold ' +
      'nobuiltin noduplicate nonlazybind optnone returns_twice ' +
      'sanitize_address sanitize_memory sanitize_thread sspstrong ' +
      'uwtable returned type opaque eq ne slt sgt ' +
      'sle sge ult ugt ule uge oeq one olt ogt ' +
      'ole oge ord uno ueq une x acq_rel acquire ' +
      'alignstack atomic catch cleanup filter inteldialect ' +
      'max min monotonic nand personality release seq_cst ' +
      'singlethread umax umin unordered xchg add fadd ' +
      'sub fsub mul fmul udiv sdiv fdiv urem srem ' +
      'frem shl lshr ashr and or xor icmp fcmp ' +
      'phi call trunc zext sext fptrunc fpext uitofp ' +
      'sitofp fptoui fptosi inttoptr ptrtoint bitcast ' +
      'addrspacecast select va_arg ret br switch invoke ' +
      'unwind unreachable indirectbr landingpad resume ' +
      'malloc alloca free load store getelementptr ' +
      'extractelement insertelement shufflevector getresult ' +
      'extractvalue insertvalue atomicrmw cmpxchg fence ' +
      'argmemonly double',
    contains: [
      TYPE,
      // this matches "empty comments"...
      // ...because it's far more likely this is a statement terminator in
      // another language than an actual comment
      hljs.COMMENT(/;\s*$/, null, { relevance: 0 }),
      hljs.COMMENT(/;/, /$/),
      hljs.QUOTE_STRING_MODE,
      {
        className: 'string',
        variants: [
          // Double-quoted string
          { begin: /"/, end: /[^\\]"/ },
        ]
      },
      FUNCTION,
      PUNCTUATION,
      OPERATOR,
      VARIABLE,
      LABEL,
      NUMBER
    ]
  };
}

module.exports = llvm;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbGx2bS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBLFdBQVcsUUFBUTtBQUNuQixhQUFhO0FBQ2I7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBLFdBQVcsdUJBQXVCO0FBQ2xDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFVBQVUsNEJBQTRCO0FBQ3RDLFVBQVU7QUFDVjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxVQUFVLHNCQUFzQjtBQUNoQztBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxRQUFRLDhCQUE4QjtBQUN0QyxRQUFRLGVBQWU7QUFDdkIsUUFBUSxlQUFlO0FBQ3ZCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxRQUFRLDhCQUE4QjtBQUN0QyxRQUFRLGVBQWU7QUFDdkIsUUFBUSw4QkFBOEI7QUFDdEMsUUFBUSxpQ0FBaUM7QUFDekM7QUFDQTtBQUNBLFFBQVE7QUFDUjtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EscUJBQXFCLGVBQWUsY0FBYztBQUNsRCxxQkFBcUI7QUFDckI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFlBQVksMkJBQTJCO0FBQ3ZDO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvbGx2bS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKipcbiAqIEBwYXJhbSB7c3RyaW5nfSB2YWx1ZVxuICogQHJldHVybnMge1JlZ0V4cH1cbiAqICovXG5cbi8qKlxuICogQHBhcmFtIHtSZWdFeHAgfCBzdHJpbmcgfSByZVxuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gc291cmNlKHJlKSB7XG4gIGlmICghcmUpIHJldHVybiBudWxsO1xuICBpZiAodHlwZW9mIHJlID09PSBcInN0cmluZ1wiKSByZXR1cm4gcmU7XG5cbiAgcmV0dXJuIHJlLnNvdXJjZTtcbn1cblxuLyoqXG4gKiBAcGFyYW0gey4uLihSZWdFeHAgfCBzdHJpbmcpIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gY29uY2F0KC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcIlwiKTtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLypcbkxhbmd1YWdlOiBMTFZNIElSXG5BdXRob3I6IE1pY2hhZWwgUm9kbGVyIDxjb250YWN0QGYwcmtpLmF0PlxuRGVzY3JpcHRpb246IGxhbmd1YWdlIHVzZWQgYXMgaW50ZXJtZWRpYXRlIHJlcHJlc2VudGF0aW9uIGluIHRoZSBMTFZNIGNvbXBpbGVyIGZyYW1ld29ya1xuV2Vic2l0ZTogaHR0cHM6Ly9sbHZtLm9yZy9kb2NzL0xhbmdSZWYuaHRtbFxuQ2F0ZWdvcnk6IGFzc2VtYmxlclxuQXVkaXQ6IDIwMjBcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBsbHZtKGhsanMpIHtcbiAgY29uc3QgSURFTlRfUkUgPSAvKFstYS16QS1aJC5fXVtcXHckLi1dKikvO1xuICBjb25zdCBUWVBFID0ge1xuICAgIGNsYXNzTmFtZTogJ3R5cGUnLFxuICAgIGJlZ2luOiAvXFxiaVxcZCsoPz1cXHN8XFxiKS9cbiAgfTtcbiAgY29uc3QgT1BFUkFUT1IgPSB7XG4gICAgY2xhc3NOYW1lOiAnb3BlcmF0b3InLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBiZWdpbjogLz0vXG4gIH07XG4gIGNvbnN0IFBVTkNUVUFUSU9OID0ge1xuICAgIGNsYXNzTmFtZTogJ3B1bmN0dWF0aW9uJyxcbiAgICByZWxldmFuY2U6IDAsXG4gICAgYmVnaW46IC8sL1xuICB9O1xuICBjb25zdCBOVU1CRVIgPSB7XG4gICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICB2YXJpYW50czogW1xuICAgICAgICB7IGJlZ2luOiAvMFt4WF1bYS1mQS1GMC05XSsvIH0sXG4gICAgICAgIHsgYmVnaW46IC8tP1xcZCsoPzpbLl1cXGQrKT8oPzpbZUVdWy0rXT9cXGQrKD86Wy5dXFxkKyk/KT8vIH1cbiAgICBdLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICBjb25zdCBMQUJFTCA9IHtcbiAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICAgIHsgYmVnaW46IC9eXFxzKlthLXpdKzovIH0sIC8vIGxhYmVsc1xuICAgIF0sXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG4gIGNvbnN0IFZBUklBQkxFID0ge1xuICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICB2YXJpYW50czogW1xuICAgICAgeyBiZWdpbjogY29uY2F0KC8lLywgSURFTlRfUkUpIH0sXG4gICAgICB7IGJlZ2luOiAvJVxcZCsvIH0sXG4gICAgICB7IGJlZ2luOiAvI1xcZCsvIH0sXG4gICAgXVxuICB9O1xuICBjb25zdCBGVU5DVElPTiA9IHtcbiAgICBjbGFzc05hbWU6ICd0aXRsZScsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHsgYmVnaW46IGNvbmNhdCgvQC8sIElERU5UX1JFKSB9LFxuICAgICAgeyBiZWdpbjogL0BcXGQrLyB9LFxuICAgICAgeyBiZWdpbjogY29uY2F0KC8hLywgSURFTlRfUkUpIH0sXG4gICAgICB7IGJlZ2luOiBjb25jYXQoLyFcXGQrLywgSURFTlRfUkUpIH0sXG4gICAgICAvLyBodHRwczovL2xsdm0ub3JnL2RvY3MvTGFuZ1JlZi5odG1sI25hbWVkbWV0YWRhdGFzdHJ1Y3R1cmVcbiAgICAgIC8vIG9idmlvdXNseSBhIHNpbmdsZSBkaWdpdCBjYW4gYWxzbyBiZSB1c2VkIGluIHRoaXMgZmFzaGlvblxuICAgICAgeyBiZWdpbjogLyFcXGQrLyB9XG4gICAgXVxuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0xMVk0gSVInLFxuICAgIC8vIFRPRE86IHNwbGl0IGludG8gZGlmZmVyZW50IGNhdGVnb3JpZXMgb2Yga2V5d29yZHNcbiAgICBrZXl3b3JkczpcbiAgICAgICdiZWdpbiBlbmQgdHJ1ZSBmYWxzZSBkZWNsYXJlIGRlZmluZSBnbG9iYWwgJyArXG4gICAgICAnY29uc3RhbnQgcHJpdmF0ZSBsaW5rZXJfcHJpdmF0ZSBpbnRlcm5hbCAnICtcbiAgICAgICdhdmFpbGFibGVfZXh0ZXJuYWxseSBsaW5rb25jZSBsaW5rb25jZV9vZHIgd2VhayAnICtcbiAgICAgICd3ZWFrX29kciBhcHBlbmRpbmcgZGxsaW1wb3J0IGRsbGV4cG9ydCBjb21tb24gJyArXG4gICAgICAnZGVmYXVsdCBoaWRkZW4gcHJvdGVjdGVkIGV4dGVybl93ZWFrIGV4dGVybmFsICcgK1xuICAgICAgJ3RocmVhZF9sb2NhbCB6ZXJvaW5pdGlhbGl6ZXIgdW5kZWYgbnVsbCB0byB0YWlsICcgK1xuICAgICAgJ3RhcmdldCB0cmlwbGUgZGF0YWxheW91dCB2b2xhdGlsZSBudXcgbnN3IG5uYW4gJyArXG4gICAgICAnbmluZiBuc3ogYXJjcCBmYXN0IGV4YWN0IGluYm91bmRzIGFsaWduICcgK1xuICAgICAgJ2FkZHJzcGFjZSBzZWN0aW9uIGFsaWFzIG1vZHVsZSBhc20gc2lkZWVmZmVjdCAnICtcbiAgICAgICdnYyBkYmcgbGlua2VyX3ByaXZhdGVfd2VhayBhdHRyaWJ1dGVzIGJsb2NrYWRkcmVzcyAnICtcbiAgICAgICdpbml0aWFsZXhlYyBsb2NhbGR5bmFtaWMgbG9jYWxleGVjIHByZWZpeCB1bm5hbWVkX2FkZHIgJyArXG4gICAgICAnY2NjIGZhc3RjYyBjb2xkY2MgeDg2X3N0ZGNhbGxjYyB4ODZfZmFzdGNhbGxjYyAnICtcbiAgICAgICdhcm1fYXBjc2NjIGFybV9hYXBjc2NjIGFybV9hYXBjc192ZnBjYyBwdHhfZGV2aWNlICcgK1xuICAgICAgJ3B0eF9rZXJuZWwgaW50ZWxfb2NsX2JpY2MgbXNwNDMwX2ludHJjYyBzcGlyX2Z1bmMgJyArXG4gICAgICAnc3Bpcl9rZXJuZWwgeDg2XzY0X3N5c3ZjYyB4ODZfNjRfd2luNjRjYyB4ODZfdGhpc2NhbGxjYyAnICtcbiAgICAgICdjYyBjIHNpZ25leHQgemVyb2V4dCBpbnJlZyBzcmV0IG5vdW53aW5kICcgK1xuICAgICAgJ25vcmV0dXJuIG5vYWxpYXMgbm9jYXB0dXJlIGJ5dmFsIG5lc3QgcmVhZG5vbmUgJyArXG4gICAgICAncmVhZG9ubHkgaW5saW5laGludCBub2lubGluZSBhbHdheXNpbmxpbmUgb3B0c2l6ZSBzc3AgJyArXG4gICAgICAnc3NwcmVxIG5vcmVkem9uZSBub2ltcGxpY2l0ZmxvYXQgbmFrZWQgYnVpbHRpbiBjb2xkICcgK1xuICAgICAgJ25vYnVpbHRpbiBub2R1cGxpY2F0ZSBub25sYXp5YmluZCBvcHRub25lIHJldHVybnNfdHdpY2UgJyArXG4gICAgICAnc2FuaXRpemVfYWRkcmVzcyBzYW5pdGl6ZV9tZW1vcnkgc2FuaXRpemVfdGhyZWFkIHNzcHN0cm9uZyAnICtcbiAgICAgICd1d3RhYmxlIHJldHVybmVkIHR5cGUgb3BhcXVlIGVxIG5lIHNsdCBzZ3QgJyArXG4gICAgICAnc2xlIHNnZSB1bHQgdWd0IHVsZSB1Z2Ugb2VxIG9uZSBvbHQgb2d0ICcgK1xuICAgICAgJ29sZSBvZ2Ugb3JkIHVubyB1ZXEgdW5lIHggYWNxX3JlbCBhY3F1aXJlICcgK1xuICAgICAgJ2FsaWduc3RhY2sgYXRvbWljIGNhdGNoIGNsZWFudXAgZmlsdGVyIGludGVsZGlhbGVjdCAnICtcbiAgICAgICdtYXggbWluIG1vbm90b25pYyBuYW5kIHBlcnNvbmFsaXR5IHJlbGVhc2Ugc2VxX2NzdCAnICtcbiAgICAgICdzaW5nbGV0aHJlYWQgdW1heCB1bWluIHVub3JkZXJlZCB4Y2hnIGFkZCBmYWRkICcgK1xuICAgICAgJ3N1YiBmc3ViIG11bCBmbXVsIHVkaXYgc2RpdiBmZGl2IHVyZW0gc3JlbSAnICtcbiAgICAgICdmcmVtIHNobCBsc2hyIGFzaHIgYW5kIG9yIHhvciBpY21wIGZjbXAgJyArXG4gICAgICAncGhpIGNhbGwgdHJ1bmMgemV4dCBzZXh0IGZwdHJ1bmMgZnBleHQgdWl0b2ZwICcgK1xuICAgICAgJ3NpdG9mcCBmcHRvdWkgZnB0b3NpIGludHRvcHRyIHB0cnRvaW50IGJpdGNhc3QgJyArXG4gICAgICAnYWRkcnNwYWNlY2FzdCBzZWxlY3QgdmFfYXJnIHJldCBiciBzd2l0Y2ggaW52b2tlICcgK1xuICAgICAgJ3Vud2luZCB1bnJlYWNoYWJsZSBpbmRpcmVjdGJyIGxhbmRpbmdwYWQgcmVzdW1lICcgK1xuICAgICAgJ21hbGxvYyBhbGxvY2EgZnJlZSBsb2FkIHN0b3JlIGdldGVsZW1lbnRwdHIgJyArXG4gICAgICAnZXh0cmFjdGVsZW1lbnQgaW5zZXJ0ZWxlbWVudCBzaHVmZmxldmVjdG9yIGdldHJlc3VsdCAnICtcbiAgICAgICdleHRyYWN0dmFsdWUgaW5zZXJ0dmFsdWUgYXRvbWljcm13IGNtcHhjaGcgZmVuY2UgJyArXG4gICAgICAnYXJnbWVtb25seSBkb3VibGUnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBUWVBFLFxuICAgICAgLy8gdGhpcyBtYXRjaGVzIFwiZW1wdHkgY29tbWVudHNcIi4uLlxuICAgICAgLy8gLi4uYmVjYXVzZSBpdCdzIGZhciBtb3JlIGxpa2VseSB0aGlzIGlzIGEgc3RhdGVtZW50IHRlcm1pbmF0b3IgaW5cbiAgICAgIC8vIGFub3RoZXIgbGFuZ3VhZ2UgdGhhbiBhbiBhY3R1YWwgY29tbWVudFxuICAgICAgaGxqcy5DT01NRU5UKC87XFxzKiQvLCBudWxsLCB7IHJlbGV2YW5jZTogMCB9KSxcbiAgICAgIGhsanMuQ09NTUVOVCgvOy8sIC8kLyksXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIC8vIERvdWJsZS1xdW90ZWQgc3RyaW5nXG4gICAgICAgICAgeyBiZWdpbjogL1wiLywgZW5kOiAvW15cXFxcXVwiLyB9LFxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAgRlVOQ1RJT04sXG4gICAgICBQVU5DVFVBVElPTixcbiAgICAgIE9QRVJBVE9SLFxuICAgICAgVkFSSUFCTEUsXG4gICAgICBMQUJFTCxcbiAgICAgIE5VTUJFUlxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBsbHZtO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9