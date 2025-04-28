(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_pf"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/pf.js":
/*!*********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/pf.js ***!
  \*********************************************************************************************/
/***/ ((module) => {

/*
Language: Packet Filter config
Description: pf.conf — packet filter configuration file (OpenBSD)
Author: Peter Piwowarski <oldlaptop654@aol.com>
Website: http://man.openbsd.org/pf.conf
Category: config
*/

function pf(hljs) {
  const MACRO = {
    className: 'variable',
    begin: /\$[\w\d#@][\w\d_]*/
  };
  const TABLE = {
    className: 'variable',
    begin: /<(?!\/)/,
    end: />/
  };

  return {
    name: 'Packet Filter config',
    aliases: [ 'pf.conf' ],
    keywords: {
      $pattern: /[a-z0-9_<>-]+/,
      built_in: /* block match pass are "actions" in pf.conf(5), the rest are
                 * lexically similar top-level commands.
                 */
        'block match pass load anchor|5 antispoof|10 set table',
      keyword:
        'in out log quick on rdomain inet inet6 proto from port os to route ' +
        'allow-opts divert-packet divert-reply divert-to flags group icmp-type ' +
        'icmp6-type label once probability recieved-on rtable prio queue ' +
        'tos tag tagged user keep fragment for os drop ' +
        'af-to|10 binat-to|10 nat-to|10 rdr-to|10 bitmask least-stats random round-robin ' +
        'source-hash static-port ' +
        'dup-to reply-to route-to ' +
        'parent bandwidth default min max qlimit ' +
        'block-policy debug fingerprints hostid limit loginterface optimization ' +
        'reassemble ruleset-optimization basic none profile skip state-defaults ' +
        'state-policy timeout ' +
        'const counters persist ' +
        'no modulate synproxy state|5 floating if-bound no-sync pflow|10 sloppy ' +
        'source-track global rule max-src-nodes max-src-states max-src-conn ' +
        'max-src-conn-rate overload flush ' +
        'scrub|5 max-mss min-ttl no-df|10 random-id',
      literal:
        'all any no-route self urpf-failed egress|5 unknown'
    },
    contains: [
      hljs.HASH_COMMENT_MODE,
      hljs.NUMBER_MODE,
      hljs.QUOTE_STRING_MODE,
      MACRO,
      TABLE
    ]
  };
}

module.exports = pf;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcGYuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9wZi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFBhY2tldCBGaWx0ZXIgY29uZmlnXG5EZXNjcmlwdGlvbjogcGYuY29uZiDigJQgcGFja2V0IGZpbHRlciBjb25maWd1cmF0aW9uIGZpbGUgKE9wZW5CU0QpXG5BdXRob3I6IFBldGVyIFBpd293YXJza2kgPG9sZGxhcHRvcDY1NEBhb2wuY29tPlxuV2Vic2l0ZTogaHR0cDovL21hbi5vcGVuYnNkLm9yZy9wZi5jb25mXG5DYXRlZ29yeTogY29uZmlnXG4qL1xuXG5mdW5jdGlvbiBwZihobGpzKSB7XG4gIGNvbnN0IE1BQ1JPID0ge1xuICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICBiZWdpbjogL1xcJFtcXHdcXGQjQF1bXFx3XFxkX10qL1xuICB9O1xuICBjb25zdCBUQUJMRSA9IHtcbiAgICBjbGFzc05hbWU6ICd2YXJpYWJsZScsXG4gICAgYmVnaW46IC88KD8hXFwvKS8sXG4gICAgZW5kOiAvPi9cbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdQYWNrZXQgRmlsdGVyIGNvbmZpZycsXG4gICAgYWxpYXNlczogWyAncGYuY29uZicgXSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAgJHBhdHRlcm46IC9bYS16MC05Xzw+LV0rLyxcbiAgICAgIGJ1aWx0X2luOiAvKiBibG9jayBtYXRjaCBwYXNzIGFyZSBcImFjdGlvbnNcIiBpbiBwZi5jb25mKDUpLCB0aGUgcmVzdCBhcmVcbiAgICAgICAgICAgICAgICAgKiBsZXhpY2FsbHkgc2ltaWxhciB0b3AtbGV2ZWwgY29tbWFuZHMuXG4gICAgICAgICAgICAgICAgICovXG4gICAgICAgICdibG9jayBtYXRjaCBwYXNzIGxvYWQgYW5jaG9yfDUgYW50aXNwb29mfDEwIHNldCB0YWJsZScsXG4gICAgICBrZXl3b3JkOlxuICAgICAgICAnaW4gb3V0IGxvZyBxdWljayBvbiByZG9tYWluIGluZXQgaW5ldDYgcHJvdG8gZnJvbSBwb3J0IG9zIHRvIHJvdXRlICcgK1xuICAgICAgICAnYWxsb3ctb3B0cyBkaXZlcnQtcGFja2V0IGRpdmVydC1yZXBseSBkaXZlcnQtdG8gZmxhZ3MgZ3JvdXAgaWNtcC10eXBlICcgK1xuICAgICAgICAnaWNtcDYtdHlwZSBsYWJlbCBvbmNlIHByb2JhYmlsaXR5IHJlY2lldmVkLW9uIHJ0YWJsZSBwcmlvIHF1ZXVlICcgK1xuICAgICAgICAndG9zIHRhZyB0YWdnZWQgdXNlciBrZWVwIGZyYWdtZW50IGZvciBvcyBkcm9wICcgK1xuICAgICAgICAnYWYtdG98MTAgYmluYXQtdG98MTAgbmF0LXRvfDEwIHJkci10b3wxMCBiaXRtYXNrIGxlYXN0LXN0YXRzIHJhbmRvbSByb3VuZC1yb2JpbiAnICtcbiAgICAgICAgJ3NvdXJjZS1oYXNoIHN0YXRpYy1wb3J0ICcgK1xuICAgICAgICAnZHVwLXRvIHJlcGx5LXRvIHJvdXRlLXRvICcgK1xuICAgICAgICAncGFyZW50IGJhbmR3aWR0aCBkZWZhdWx0IG1pbiBtYXggcWxpbWl0ICcgK1xuICAgICAgICAnYmxvY2stcG9saWN5IGRlYnVnIGZpbmdlcnByaW50cyBob3N0aWQgbGltaXQgbG9naW50ZXJmYWNlIG9wdGltaXphdGlvbiAnICtcbiAgICAgICAgJ3JlYXNzZW1ibGUgcnVsZXNldC1vcHRpbWl6YXRpb24gYmFzaWMgbm9uZSBwcm9maWxlIHNraXAgc3RhdGUtZGVmYXVsdHMgJyArXG4gICAgICAgICdzdGF0ZS1wb2xpY3kgdGltZW91dCAnICtcbiAgICAgICAgJ2NvbnN0IGNvdW50ZXJzIHBlcnNpc3QgJyArXG4gICAgICAgICdubyBtb2R1bGF0ZSBzeW5wcm94eSBzdGF0ZXw1IGZsb2F0aW5nIGlmLWJvdW5kIG5vLXN5bmMgcGZsb3d8MTAgc2xvcHB5ICcgK1xuICAgICAgICAnc291cmNlLXRyYWNrIGdsb2JhbCBydWxlIG1heC1zcmMtbm9kZXMgbWF4LXNyYy1zdGF0ZXMgbWF4LXNyYy1jb25uICcgK1xuICAgICAgICAnbWF4LXNyYy1jb25uLXJhdGUgb3ZlcmxvYWQgZmx1c2ggJyArXG4gICAgICAgICdzY3J1Ynw1IG1heC1tc3MgbWluLXR0bCBuby1kZnwxMCByYW5kb20taWQnLFxuICAgICAgbGl0ZXJhbDpcbiAgICAgICAgJ2FsbCBhbnkgbm8tcm91dGUgc2VsZiB1cnBmLWZhaWxlZCBlZ3Jlc3N8NSB1bmtub3duJ1xuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgICBobGpzLk5VTUJFUl9NT0RFLFxuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgIE1BQ1JPLFxuICAgICAgVEFCTEVcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gcGY7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=