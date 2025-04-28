(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_gradle"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/gradle.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/gradle.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Gradle
Description: Gradle is an open-source build automation tool focused on flexibility and performance.
Website: https://gradle.org
Author: Damian Mee <mee.damian@gmail.com>
*/

function gradle(hljs) {
  return {
    name: 'Gradle',
    case_insensitive: true,
    keywords: {
      keyword:
        'task project allprojects subprojects artifacts buildscript configurations ' +
        'dependencies repositories sourceSets description delete from into include ' +
        'exclude source classpath destinationDir includes options sourceCompatibility ' +
        'targetCompatibility group flatDir doLast doFirst flatten todir fromdir ant ' +
        'def abstract break case catch continue default do else extends final finally ' +
        'for if implements instanceof native new private protected public return static ' +
        'switch synchronized throw throws transient try volatile while strictfp package ' +
        'import false null super this true antlrtask checkstyle codenarc copy boolean ' +
        'byte char class double float int interface long short void compile runTime ' +
        'file fileTree abs any append asList asWritable call collect compareTo count ' +
        'div dump each eachByte eachFile eachLine every find findAll flatten getAt ' +
        'getErr getIn getOut getText grep immutable inject inspect intersect invokeMethods ' +
        'isCase join leftShift minus multiply newInputStream newOutputStream newPrintWriter ' +
        'newReader newWriter next plus pop power previous print println push putAt read ' +
        'readBytes readLines reverse reverseEach round size sort splitEachLine step subMap ' +
        'times toInteger toList tokenize upto waitForOrKill withPrintWriter withReader ' +
        'withStream withWriter withWriterAppend write writeLine'
    },
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.NUMBER_MODE,
      hljs.REGEXP_MODE

    ]
  };
}

module.exports = gradle;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZ3JhZGxlLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvZ3JhZGxlLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogR3JhZGxlXG5EZXNjcmlwdGlvbjogR3JhZGxlIGlzIGFuIG9wZW4tc291cmNlIGJ1aWxkIGF1dG9tYXRpb24gdG9vbCBmb2N1c2VkIG9uIGZsZXhpYmlsaXR5IGFuZCBwZXJmb3JtYW5jZS5cbldlYnNpdGU6IGh0dHBzOi8vZ3JhZGxlLm9yZ1xuQXV0aG9yOiBEYW1pYW4gTWVlIDxtZWUuZGFtaWFuQGdtYWlsLmNvbT5cbiovXG5cbmZ1bmN0aW9uIGdyYWRsZShobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0dyYWRsZScsXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAga2V5d29yZDpcbiAgICAgICAgJ3Rhc2sgcHJvamVjdCBhbGxwcm9qZWN0cyBzdWJwcm9qZWN0cyBhcnRpZmFjdHMgYnVpbGRzY3JpcHQgY29uZmlndXJhdGlvbnMgJyArXG4gICAgICAgICdkZXBlbmRlbmNpZXMgcmVwb3NpdG9yaWVzIHNvdXJjZVNldHMgZGVzY3JpcHRpb24gZGVsZXRlIGZyb20gaW50byBpbmNsdWRlICcgK1xuICAgICAgICAnZXhjbHVkZSBzb3VyY2UgY2xhc3NwYXRoIGRlc3RpbmF0aW9uRGlyIGluY2x1ZGVzIG9wdGlvbnMgc291cmNlQ29tcGF0aWJpbGl0eSAnICtcbiAgICAgICAgJ3RhcmdldENvbXBhdGliaWxpdHkgZ3JvdXAgZmxhdERpciBkb0xhc3QgZG9GaXJzdCBmbGF0dGVuIHRvZGlyIGZyb21kaXIgYW50ICcgK1xuICAgICAgICAnZGVmIGFic3RyYWN0IGJyZWFrIGNhc2UgY2F0Y2ggY29udGludWUgZGVmYXVsdCBkbyBlbHNlIGV4dGVuZHMgZmluYWwgZmluYWxseSAnICtcbiAgICAgICAgJ2ZvciBpZiBpbXBsZW1lbnRzIGluc3RhbmNlb2YgbmF0aXZlIG5ldyBwcml2YXRlIHByb3RlY3RlZCBwdWJsaWMgcmV0dXJuIHN0YXRpYyAnICtcbiAgICAgICAgJ3N3aXRjaCBzeW5jaHJvbml6ZWQgdGhyb3cgdGhyb3dzIHRyYW5zaWVudCB0cnkgdm9sYXRpbGUgd2hpbGUgc3RyaWN0ZnAgcGFja2FnZSAnICtcbiAgICAgICAgJ2ltcG9ydCBmYWxzZSBudWxsIHN1cGVyIHRoaXMgdHJ1ZSBhbnRscnRhc2sgY2hlY2tzdHlsZSBjb2RlbmFyYyBjb3B5IGJvb2xlYW4gJyArXG4gICAgICAgICdieXRlIGNoYXIgY2xhc3MgZG91YmxlIGZsb2F0IGludCBpbnRlcmZhY2UgbG9uZyBzaG9ydCB2b2lkIGNvbXBpbGUgcnVuVGltZSAnICtcbiAgICAgICAgJ2ZpbGUgZmlsZVRyZWUgYWJzIGFueSBhcHBlbmQgYXNMaXN0IGFzV3JpdGFibGUgY2FsbCBjb2xsZWN0IGNvbXBhcmVUbyBjb3VudCAnICtcbiAgICAgICAgJ2RpdiBkdW1wIGVhY2ggZWFjaEJ5dGUgZWFjaEZpbGUgZWFjaExpbmUgZXZlcnkgZmluZCBmaW5kQWxsIGZsYXR0ZW4gZ2V0QXQgJyArXG4gICAgICAgICdnZXRFcnIgZ2V0SW4gZ2V0T3V0IGdldFRleHQgZ3JlcCBpbW11dGFibGUgaW5qZWN0IGluc3BlY3QgaW50ZXJzZWN0IGludm9rZU1ldGhvZHMgJyArXG4gICAgICAgICdpc0Nhc2Ugam9pbiBsZWZ0U2hpZnQgbWludXMgbXVsdGlwbHkgbmV3SW5wdXRTdHJlYW0gbmV3T3V0cHV0U3RyZWFtIG5ld1ByaW50V3JpdGVyICcgK1xuICAgICAgICAnbmV3UmVhZGVyIG5ld1dyaXRlciBuZXh0IHBsdXMgcG9wIHBvd2VyIHByZXZpb3VzIHByaW50IHByaW50bG4gcHVzaCBwdXRBdCByZWFkICcgK1xuICAgICAgICAncmVhZEJ5dGVzIHJlYWRMaW5lcyByZXZlcnNlIHJldmVyc2VFYWNoIHJvdW5kIHNpemUgc29ydCBzcGxpdEVhY2hMaW5lIHN0ZXAgc3ViTWFwICcgK1xuICAgICAgICAndGltZXMgdG9JbnRlZ2VyIHRvTGlzdCB0b2tlbml6ZSB1cHRvIHdhaXRGb3JPcktpbGwgd2l0aFByaW50V3JpdGVyIHdpdGhSZWFkZXIgJyArXG4gICAgICAgICd3aXRoU3RyZWFtIHdpdGhXcml0ZXIgd2l0aFdyaXRlckFwcGVuZCB3cml0ZSB3cml0ZUxpbmUnXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBobGpzLk5VTUJFUl9NT0RFLFxuICAgICAgaGxqcy5SRUdFWFBfTU9ERVxuXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGdyYWRsZTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==