(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_matlab"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/matlab.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/matlab.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Matlab
Author: Denis Bardadym <bardadymchik@gmail.com>
Contributors: Eugene Nizhibitsky <nizhibitsky@ya.ru>, Egor Rogov <e.rogov@postgrespro.ru>
Website: https://www.mathworks.com/products/matlab.html
Category: scientific
*/

/*
  Formal syntax is not published, helpful link:
  https://github.com/kornilova-l/matlab-IntelliJ-plugin/blob/master/src/main/grammar/Matlab.bnf
*/
function matlab(hljs) {

  var TRANSPOSE_RE = '(\'|\\.\')+';
  var TRANSPOSE = {
    relevance: 0,
    contains: [
      { begin: TRANSPOSE_RE }
    ]
  };

  return {
    name: 'Matlab',
    keywords: {
      keyword:
        'arguments break case catch classdef continue else elseif end enumeration events for function ' +
        'global if methods otherwise parfor persistent properties return spmd switch try while',
      built_in:
        'sin sind sinh asin asind asinh cos cosd cosh acos acosd acosh tan tand tanh atan ' +
        'atand atan2 atanh sec secd sech asec asecd asech csc cscd csch acsc acscd acsch cot ' +
        'cotd coth acot acotd acoth hypot exp expm1 log log1p log10 log2 pow2 realpow reallog ' +
        'realsqrt sqrt nthroot nextpow2 abs angle complex conj imag real unwrap isreal ' +
        'cplxpair fix floor ceil round mod rem sign airy besselj bessely besselh besseli ' +
        'besselk beta betainc betaln ellipj ellipke erf erfc erfcx erfinv expint gamma ' +
        'gammainc gammaln psi legendre cross dot factor isprime primes gcd lcm rat rats perms ' +
        'nchoosek factorial cart2sph cart2pol pol2cart sph2cart hsv2rgb rgb2hsv zeros ones ' +
        'eye repmat rand randn linspace logspace freqspace meshgrid accumarray size length ' +
        'ndims numel disp isempty isequal isequalwithequalnans cat reshape diag blkdiag tril ' +
        'triu fliplr flipud flipdim rot90 find sub2ind ind2sub bsxfun ndgrid permute ipermute ' +
        'shiftdim circshift squeeze isscalar isvector ans eps realmax realmin pi i|0 inf nan ' +
        'isnan isinf isfinite j|0 why compan gallery hadamard hankel hilb invhilb magic pascal ' +
        'rosser toeplitz vander wilkinson max min nanmax nanmin mean nanmean type table ' +
        'readtable writetable sortrows sort figure plot plot3 scatter scatter3 cellfun ' +
        'legend intersect ismember procrustes hold num2cell '
    },
    illegal: '(//|"|#|/\\*|\\s+/\\w+)',
    contains: [
      {
        className: 'function',
        beginKeywords: 'function', end: '$',
        contains: [
          hljs.UNDERSCORE_TITLE_MODE,
          {
            className: 'params',
            variants: [
              {begin: '\\(', end: '\\)'},
              {begin: '\\[', end: '\\]'}
            ]
          }
        ]
      },
      {
        className: 'built_in',
        begin: /true|false/,
        relevance: 0,
        starts: TRANSPOSE
      },
      {
        begin: '[a-zA-Z][a-zA-Z_0-9]*' + TRANSPOSE_RE,
        relevance: 0
      },
      {
        className: 'number',
        begin: hljs.C_NUMBER_RE,
        relevance: 0,
        starts: TRANSPOSE
      },
      {
        className: 'string',
        begin: '\'', end: '\'',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          {begin: '\'\''}]
      },
      {
        begin: /\]|\}|\)/,
        relevance: 0,
        starts: TRANSPOSE
      },
      {
        className: 'string',
        begin: '"', end: '"',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          {begin: '""'}
        ],
        starts: TRANSPOSE
      },
      hljs.COMMENT('^\\s*%\\{\\s*$', '^\\s*%\\}\\s*$'),
      hljs.COMMENT('%', '$')
    ]
  };
}

module.exports = matlab;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbWF0bGFiLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSxRQUFRO0FBQ1I7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZUFBZSx5QkFBeUI7QUFDeEMsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXLGNBQWM7QUFDekIsT0FBTztBQUNQO0FBQ0EscUJBQXFCO0FBQ3JCO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0EsT0FBTztBQUNQLDZCQUE2QixrQkFBa0I7QUFDL0M7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL21hdGxhYi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IE1hdGxhYlxuQXV0aG9yOiBEZW5pcyBCYXJkYWR5bSA8YmFyZGFkeW1jaGlrQGdtYWlsLmNvbT5cbkNvbnRyaWJ1dG9yczogRXVnZW5lIE5pemhpYml0c2t5IDxuaXpoaWJpdHNreUB5YS5ydT4sIEVnb3IgUm9nb3YgPGUucm9nb3ZAcG9zdGdyZXNwcm8ucnU+XG5XZWJzaXRlOiBodHRwczovL3d3dy5tYXRod29ya3MuY29tL3Byb2R1Y3RzL21hdGxhYi5odG1sXG5DYXRlZ29yeTogc2NpZW50aWZpY1xuKi9cblxuLypcbiAgRm9ybWFsIHN5bnRheCBpcyBub3QgcHVibGlzaGVkLCBoZWxwZnVsIGxpbms6XG4gIGh0dHBzOi8vZ2l0aHViLmNvbS9rb3JuaWxvdmEtbC9tYXRsYWItSW50ZWxsaUotcGx1Z2luL2Jsb2IvbWFzdGVyL3NyYy9tYWluL2dyYW1tYXIvTWF0bGFiLmJuZlxuKi9cbmZ1bmN0aW9uIG1hdGxhYihobGpzKSB7XG5cbiAgdmFyIFRSQU5TUE9TRV9SRSA9ICcoXFwnfFxcXFwuXFwnKSsnO1xuICB2YXIgVFJBTlNQT1NFID0ge1xuICAgIHJlbGV2YW5jZTogMCxcbiAgICBjb250YWluczogW1xuICAgICAgeyBiZWdpbjogVFJBTlNQT1NFX1JFIH1cbiAgICBdXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnTWF0bGFiJyxcbiAgICBrZXl3b3Jkczoge1xuICAgICAga2V5d29yZDpcbiAgICAgICAgJ2FyZ3VtZW50cyBicmVhayBjYXNlIGNhdGNoIGNsYXNzZGVmIGNvbnRpbnVlIGVsc2UgZWxzZWlmIGVuZCBlbnVtZXJhdGlvbiBldmVudHMgZm9yIGZ1bmN0aW9uICcgK1xuICAgICAgICAnZ2xvYmFsIGlmIG1ldGhvZHMgb3RoZXJ3aXNlIHBhcmZvciBwZXJzaXN0ZW50IHByb3BlcnRpZXMgcmV0dXJuIHNwbWQgc3dpdGNoIHRyeSB3aGlsZScsXG4gICAgICBidWlsdF9pbjpcbiAgICAgICAgJ3NpbiBzaW5kIHNpbmggYXNpbiBhc2luZCBhc2luaCBjb3MgY29zZCBjb3NoIGFjb3MgYWNvc2QgYWNvc2ggdGFuIHRhbmQgdGFuaCBhdGFuICcgK1xuICAgICAgICAnYXRhbmQgYXRhbjIgYXRhbmggc2VjIHNlY2Qgc2VjaCBhc2VjIGFzZWNkIGFzZWNoIGNzYyBjc2NkIGNzY2ggYWNzYyBhY3NjZCBhY3NjaCBjb3QgJyArXG4gICAgICAgICdjb3RkIGNvdGggYWNvdCBhY290ZCBhY290aCBoeXBvdCBleHAgZXhwbTEgbG9nIGxvZzFwIGxvZzEwIGxvZzIgcG93MiByZWFscG93IHJlYWxsb2cgJyArXG4gICAgICAgICdyZWFsc3FydCBzcXJ0IG50aHJvb3QgbmV4dHBvdzIgYWJzIGFuZ2xlIGNvbXBsZXggY29uaiBpbWFnIHJlYWwgdW53cmFwIGlzcmVhbCAnICtcbiAgICAgICAgJ2NwbHhwYWlyIGZpeCBmbG9vciBjZWlsIHJvdW5kIG1vZCByZW0gc2lnbiBhaXJ5IGJlc3NlbGogYmVzc2VseSBiZXNzZWxoIGJlc3NlbGkgJyArXG4gICAgICAgICdiZXNzZWxrIGJldGEgYmV0YWluYyBiZXRhbG4gZWxsaXBqIGVsbGlwa2UgZXJmIGVyZmMgZXJmY3ggZXJmaW52IGV4cGludCBnYW1tYSAnICtcbiAgICAgICAgJ2dhbW1haW5jIGdhbW1hbG4gcHNpIGxlZ2VuZHJlIGNyb3NzIGRvdCBmYWN0b3IgaXNwcmltZSBwcmltZXMgZ2NkIGxjbSByYXQgcmF0cyBwZXJtcyAnICtcbiAgICAgICAgJ25jaG9vc2VrIGZhY3RvcmlhbCBjYXJ0MnNwaCBjYXJ0MnBvbCBwb2wyY2FydCBzcGgyY2FydCBoc3YycmdiIHJnYjJoc3YgemVyb3Mgb25lcyAnICtcbiAgICAgICAgJ2V5ZSByZXBtYXQgcmFuZCByYW5kbiBsaW5zcGFjZSBsb2dzcGFjZSBmcmVxc3BhY2UgbWVzaGdyaWQgYWNjdW1hcnJheSBzaXplIGxlbmd0aCAnICtcbiAgICAgICAgJ25kaW1zIG51bWVsIGRpc3AgaXNlbXB0eSBpc2VxdWFsIGlzZXF1YWx3aXRoZXF1YWxuYW5zIGNhdCByZXNoYXBlIGRpYWcgYmxrZGlhZyB0cmlsICcgK1xuICAgICAgICAndHJpdSBmbGlwbHIgZmxpcHVkIGZsaXBkaW0gcm90OTAgZmluZCBzdWIyaW5kIGluZDJzdWIgYnN4ZnVuIG5kZ3JpZCBwZXJtdXRlIGlwZXJtdXRlICcgK1xuICAgICAgICAnc2hpZnRkaW0gY2lyY3NoaWZ0IHNxdWVlemUgaXNzY2FsYXIgaXN2ZWN0b3IgYW5zIGVwcyByZWFsbWF4IHJlYWxtaW4gcGkgaXwwIGluZiBuYW4gJyArXG4gICAgICAgICdpc25hbiBpc2luZiBpc2Zpbml0ZSBqfDAgd2h5IGNvbXBhbiBnYWxsZXJ5IGhhZGFtYXJkIGhhbmtlbCBoaWxiIGludmhpbGIgbWFnaWMgcGFzY2FsICcgK1xuICAgICAgICAncm9zc2VyIHRvZXBsaXR6IHZhbmRlciB3aWxraW5zb24gbWF4IG1pbiBuYW5tYXggbmFubWluIG1lYW4gbmFubWVhbiB0eXBlIHRhYmxlICcgK1xuICAgICAgICAncmVhZHRhYmxlIHdyaXRldGFibGUgc29ydHJvd3Mgc29ydCBmaWd1cmUgcGxvdCBwbG90MyBzY2F0dGVyIHNjYXR0ZXIzIGNlbGxmdW4gJyArXG4gICAgICAgICdsZWdlbmQgaW50ZXJzZWN0IGlzbWVtYmVyIHByb2NydXN0ZXMgaG9sZCBudW0yY2VsbCAnXG4gICAgfSxcbiAgICBpbGxlZ2FsOiAnKC8vfFwifCN8L1xcXFwqfFxcXFxzKy9cXFxcdyspJyxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdmdW5jdGlvbicsIGVuZDogJyQnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuVU5ERVJTQ09SRV9USVRMRV9NT0RFLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgICAgICB7YmVnaW46ICdcXFxcKCcsIGVuZDogJ1xcXFwpJ30sXG4gICAgICAgICAgICAgIHtiZWdpbjogJ1xcXFxbJywgZW5kOiAnXFxcXF0nfVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnYnVpbHRfaW4nLFxuICAgICAgICBiZWdpbjogL3RydWV8ZmFsc2UvLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIHN0YXJ0czogVFJBTlNQT1NFXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1thLXpBLVpdW2EtekEtWl8wLTldKicgKyBUUkFOU1BPU0VfUkUsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgICAgYmVnaW46IGhsanMuQ19OVU1CRVJfUkUsXG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgc3RhcnRzOiBUUkFOU1BPU0VcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgIGJlZ2luOiAnXFwnJywgZW5kOiAnXFwnJyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBobGpzLkJBQ0tTTEFTSF9FU0NBUEUsXG4gICAgICAgICAge2JlZ2luOiAnXFwnXFwnJ31dXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcXXxcXH18XFwpLyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBzdGFydHM6IFRSQU5TUE9TRVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgYmVnaW46ICdcIicsIGVuZDogJ1wiJyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBobGpzLkJBQ0tTTEFTSF9FU0NBUEUsXG4gICAgICAgICAge2JlZ2luOiAnXCJcIid9XG4gICAgICAgIF0sXG4gICAgICAgIHN0YXJ0czogVFJBTlNQT1NFXG4gICAgICB9LFxuICAgICAgaGxqcy5DT01NRU5UKCdeXFxcXHMqJVxcXFx7XFxcXHMqJCcsICdeXFxcXHMqJVxcXFx9XFxcXHMqJCcpLFxuICAgICAgaGxqcy5DT01NRU5UKCclJywgJyQnKVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBtYXRsYWI7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=