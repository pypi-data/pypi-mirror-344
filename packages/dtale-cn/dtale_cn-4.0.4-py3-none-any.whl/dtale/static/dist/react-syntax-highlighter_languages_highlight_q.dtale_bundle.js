(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_q"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/q.js":
/*!********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/q.js ***!
  \********************************************************************************************/
/***/ ((module) => {

/*
Language: Q
Description: Q is a vector-based functional paradigm programming language built into the kdb+ database.
             (K/Q/Kdb+ from Kx Systems)
Author: Sergey Vidyuk <svidyuk@gmail.com>
Website: https://kx.com/connect-with-us/developers/
*/

function q(hljs) {
  const KEYWORDS = {
    $pattern: /(`?)[A-Za-z0-9_]+\b/,
    keyword:
      'do while select delete by update from',
    literal:
      '0b 1b',
    built_in:
      'neg not null string reciprocal floor ceiling signum mod xbar xlog and or each scan over prior mmu lsq inv md5 ltime gtime count first var dev med cov cor all any rand sums prds mins maxs fills deltas ratios avgs differ prev next rank reverse iasc idesc asc desc msum mcount mavg mdev xrank mmin mmax xprev rotate distinct group where flip type key til get value attr cut set upsert raze union inter except cross sv vs sublist enlist read0 read1 hopen hclose hdel hsym hcount peach system ltrim rtrim trim lower upper ssr view tables views cols xcols keys xkey xcol xasc xdesc fkeys meta lj aj aj0 ij pj asof uj ww wj wj1 fby xgroup ungroup ej save load rsave rload show csv parse eval min max avg wavg wsum sin cos tan sum',
    type:
      '`float `double int `timestamp `timespan `datetime `time `boolean `symbol `char `byte `short `long `real `month `date `minute `second `guid'
  };

  return {
    name: 'Q',
    aliases: [
      'k',
      'kdb'
    ],
    keywords: KEYWORDS,
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.C_NUMBER_MODE
    ]
  };
}

module.exports = q;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvcS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFFcbkRlc2NyaXB0aW9uOiBRIGlzIGEgdmVjdG9yLWJhc2VkIGZ1bmN0aW9uYWwgcGFyYWRpZ20gcHJvZ3JhbW1pbmcgbGFuZ3VhZ2UgYnVpbHQgaW50byB0aGUga2RiKyBkYXRhYmFzZS5cbiAgICAgICAgICAgICAoSy9RL0tkYisgZnJvbSBLeCBTeXN0ZW1zKVxuQXV0aG9yOiBTZXJnZXkgVmlkeXVrIDxzdmlkeXVrQGdtYWlsLmNvbT5cbldlYnNpdGU6IGh0dHBzOi8va3guY29tL2Nvbm5lY3Qtd2l0aC11cy9kZXZlbG9wZXJzL1xuKi9cblxuZnVuY3Rpb24gcShobGpzKSB7XG4gIGNvbnN0IEtFWVdPUkRTID0ge1xuICAgICRwYXR0ZXJuOiAvKGA/KVtBLVphLXowLTlfXStcXGIvLFxuICAgIGtleXdvcmQ6XG4gICAgICAnZG8gd2hpbGUgc2VsZWN0IGRlbGV0ZSBieSB1cGRhdGUgZnJvbScsXG4gICAgbGl0ZXJhbDpcbiAgICAgICcwYiAxYicsXG4gICAgYnVpbHRfaW46XG4gICAgICAnbmVnIG5vdCBudWxsIHN0cmluZyByZWNpcHJvY2FsIGZsb29yIGNlaWxpbmcgc2lnbnVtIG1vZCB4YmFyIHhsb2cgYW5kIG9yIGVhY2ggc2NhbiBvdmVyIHByaW9yIG1tdSBsc3EgaW52IG1kNSBsdGltZSBndGltZSBjb3VudCBmaXJzdCB2YXIgZGV2IG1lZCBjb3YgY29yIGFsbCBhbnkgcmFuZCBzdW1zIHByZHMgbWlucyBtYXhzIGZpbGxzIGRlbHRhcyByYXRpb3MgYXZncyBkaWZmZXIgcHJldiBuZXh0IHJhbmsgcmV2ZXJzZSBpYXNjIGlkZXNjIGFzYyBkZXNjIG1zdW0gbWNvdW50IG1hdmcgbWRldiB4cmFuayBtbWluIG1tYXggeHByZXYgcm90YXRlIGRpc3RpbmN0IGdyb3VwIHdoZXJlIGZsaXAgdHlwZSBrZXkgdGlsIGdldCB2YWx1ZSBhdHRyIGN1dCBzZXQgdXBzZXJ0IHJhemUgdW5pb24gaW50ZXIgZXhjZXB0IGNyb3NzIHN2IHZzIHN1Ymxpc3QgZW5saXN0IHJlYWQwIHJlYWQxIGhvcGVuIGhjbG9zZSBoZGVsIGhzeW0gaGNvdW50IHBlYWNoIHN5c3RlbSBsdHJpbSBydHJpbSB0cmltIGxvd2VyIHVwcGVyIHNzciB2aWV3IHRhYmxlcyB2aWV3cyBjb2xzIHhjb2xzIGtleXMgeGtleSB4Y29sIHhhc2MgeGRlc2MgZmtleXMgbWV0YSBsaiBhaiBhajAgaWogcGogYXNvZiB1aiB3dyB3aiB3ajEgZmJ5IHhncm91cCB1bmdyb3VwIGVqIHNhdmUgbG9hZCByc2F2ZSBybG9hZCBzaG93IGNzdiBwYXJzZSBldmFsIG1pbiBtYXggYXZnIHdhdmcgd3N1bSBzaW4gY29zIHRhbiBzdW0nLFxuICAgIHR5cGU6XG4gICAgICAnYGZsb2F0IGBkb3VibGUgaW50IGB0aW1lc3RhbXAgYHRpbWVzcGFuIGBkYXRldGltZSBgdGltZSBgYm9vbGVhbiBgc3ltYm9sIGBjaGFyIGBieXRlIGBzaG9ydCBgbG9uZyBgcmVhbCBgbW9udGggYGRhdGUgYG1pbnV0ZSBgc2Vjb25kIGBndWlkJ1xuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1EnLFxuICAgIGFsaWFzZXM6IFtcbiAgICAgICdrJyxcbiAgICAgICdrZGInXG4gICAgXSxcbiAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBobGpzLkNfTlVNQkVSX01PREVcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gcTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==