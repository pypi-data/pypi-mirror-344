(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_coq"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/coq.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/coq.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: Coq
Author: Stephan Boyer <stephan@stephanboyer.com>
Category: functional
Website: https://coq.inria.fr
*/

/** @type LanguageFn */
function coq(hljs) {
  return {
    name: 'Coq',
    keywords: {
      keyword:
        '_|0 as at cofix else end exists exists2 fix for forall fun if IF in let ' +
        'match mod Prop return Set then Type using where with ' +
        'Abort About Add Admit Admitted All Arguments Assumptions Axiom Back BackTo ' +
        'Backtrack Bind Blacklist Canonical Cd Check Class Classes Close Coercion ' +
        'Coercions CoFixpoint CoInductive Collection Combined Compute Conjecture ' +
        'Conjectures Constant constr Constraint Constructors Context Corollary ' +
        'CreateHintDb Cut Declare Defined Definition Delimit Dependencies Dependent ' +
        'Derive Drop eauto End Equality Eval Example Existential Existentials ' +
        'Existing Export exporting Extern Extract Extraction Fact Field Fields File ' +
        'Fixpoint Focus for From Function Functional Generalizable Global Goal Grab ' +
        'Grammar Graph Guarded Heap Hint HintDb Hints Hypotheses Hypothesis ident ' +
        'Identity If Immediate Implicit Import Include Inductive Infix Info Initial ' +
        'Inline Inspect Instance Instances Intro Intros Inversion Inversion_clear ' +
        'Language Left Lemma Let Libraries Library Load LoadPath Local Locate Ltac ML ' +
        'Mode Module Modules Monomorphic Morphism Next NoInline Notation Obligation ' +
        'Obligations Opaque Open Optimize Options Parameter Parameters Parametric ' +
        'Path Paths pattern Polymorphic Preterm Print Printing Program Projections ' +
        'Proof Proposition Pwd Qed Quit Rec Record Recursive Redirect Relation Remark ' +
        'Remove Require Reserved Reset Resolve Restart Rewrite Right Ring Rings Save ' +
        'Scheme Scope Scopes Script Search SearchAbout SearchHead SearchPattern ' +
        'SearchRewrite Section Separate Set Setoid Show Solve Sorted Step Strategies ' +
        'Strategy Structure SubClass Table Tables Tactic Term Test Theorem Time ' +
        'Timeout Transparent Type Typeclasses Types Undelimit Undo Unfocus Unfocused ' +
        'Unfold Universe Universes Unset Unshelve using Variable Variables Variant ' +
        'Verbose Visibility where with',
      built_in:
        'abstract absurd admit after apply as assert assumption at auto autorewrite ' +
        'autounfold before bottom btauto by case case_eq cbn cbv change ' +
        'classical_left classical_right clear clearbody cofix compare compute ' +
        'congruence constr_eq constructor contradict contradiction cut cutrewrite ' +
        'cycle decide decompose dependent destruct destruction dintuition ' +
        'discriminate discrR do double dtauto eapply eassumption eauto ecase ' +
        'econstructor edestruct ediscriminate eelim eexact eexists einduction ' +
        'einjection eleft elim elimtype enough equality erewrite eright ' +
        'esimplify_eq esplit evar exact exactly_once exfalso exists f_equal fail ' +
        'field field_simplify field_simplify_eq first firstorder fix fold fourier ' +
        'functional generalize generalizing gfail give_up has_evar hnf idtac in ' +
        'induction injection instantiate intro intro_pattern intros intuition ' +
        'inversion inversion_clear is_evar is_var lapply lazy left lia lra move ' +
        'native_compute nia nsatz omega once pattern pose progress proof psatz quote ' +
        'record red refine reflexivity remember rename repeat replace revert ' +
        'revgoals rewrite rewrite_strat right ring ring_simplify rtauto set ' +
        'setoid_reflexivity setoid_replace setoid_rewrite setoid_symmetry ' +
        'setoid_transitivity shelve shelve_unifiable simpl simple simplify_eq solve ' +
        'specialize split split_Rabs split_Rmult stepl stepr subst sum swap ' +
        'symmetry tactic tauto time timeout top transitivity trivial try tryif ' +
        'unfold unify until using vm_compute with'
    },
    contains: [
      hljs.QUOTE_STRING_MODE,
      hljs.COMMENT('\\(\\*', '\\*\\)'),
      hljs.C_NUMBER_MODE,
      {
        className: 'type',
        excludeBegin: true,
        begin: '\\|\\s*',
        end: '\\w+'
      },
      { // relevance booster
        begin: /[-=]>/
      }
    ]
  };
}

module.exports = coq;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY29xLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUCxRQUFRO0FBQ1I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvY29xLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogQ29xXG5BdXRob3I6IFN0ZXBoYW4gQm95ZXIgPHN0ZXBoYW5Ac3RlcGhhbmJveWVyLmNvbT5cbkNhdGVnb3J5OiBmdW5jdGlvbmFsXG5XZWJzaXRlOiBodHRwczovL2NvcS5pbnJpYS5mclxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGNvcShobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0NvcScsXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGtleXdvcmQ6XG4gICAgICAgICdffDAgYXMgYXQgY29maXggZWxzZSBlbmQgZXhpc3RzIGV4aXN0czIgZml4IGZvciBmb3JhbGwgZnVuIGlmIElGIGluIGxldCAnICtcbiAgICAgICAgJ21hdGNoIG1vZCBQcm9wIHJldHVybiBTZXQgdGhlbiBUeXBlIHVzaW5nIHdoZXJlIHdpdGggJyArXG4gICAgICAgICdBYm9ydCBBYm91dCBBZGQgQWRtaXQgQWRtaXR0ZWQgQWxsIEFyZ3VtZW50cyBBc3N1bXB0aW9ucyBBeGlvbSBCYWNrIEJhY2tUbyAnICtcbiAgICAgICAgJ0JhY2t0cmFjayBCaW5kIEJsYWNrbGlzdCBDYW5vbmljYWwgQ2QgQ2hlY2sgQ2xhc3MgQ2xhc3NlcyBDbG9zZSBDb2VyY2lvbiAnICtcbiAgICAgICAgJ0NvZXJjaW9ucyBDb0ZpeHBvaW50IENvSW5kdWN0aXZlIENvbGxlY3Rpb24gQ29tYmluZWQgQ29tcHV0ZSBDb25qZWN0dXJlICcgK1xuICAgICAgICAnQ29uamVjdHVyZXMgQ29uc3RhbnQgY29uc3RyIENvbnN0cmFpbnQgQ29uc3RydWN0b3JzIENvbnRleHQgQ29yb2xsYXJ5ICcgK1xuICAgICAgICAnQ3JlYXRlSGludERiIEN1dCBEZWNsYXJlIERlZmluZWQgRGVmaW5pdGlvbiBEZWxpbWl0IERlcGVuZGVuY2llcyBEZXBlbmRlbnQgJyArXG4gICAgICAgICdEZXJpdmUgRHJvcCBlYXV0byBFbmQgRXF1YWxpdHkgRXZhbCBFeGFtcGxlIEV4aXN0ZW50aWFsIEV4aXN0ZW50aWFscyAnICtcbiAgICAgICAgJ0V4aXN0aW5nIEV4cG9ydCBleHBvcnRpbmcgRXh0ZXJuIEV4dHJhY3QgRXh0cmFjdGlvbiBGYWN0IEZpZWxkIEZpZWxkcyBGaWxlICcgK1xuICAgICAgICAnRml4cG9pbnQgRm9jdXMgZm9yIEZyb20gRnVuY3Rpb24gRnVuY3Rpb25hbCBHZW5lcmFsaXphYmxlIEdsb2JhbCBHb2FsIEdyYWIgJyArXG4gICAgICAgICdHcmFtbWFyIEdyYXBoIEd1YXJkZWQgSGVhcCBIaW50IEhpbnREYiBIaW50cyBIeXBvdGhlc2VzIEh5cG90aGVzaXMgaWRlbnQgJyArXG4gICAgICAgICdJZGVudGl0eSBJZiBJbW1lZGlhdGUgSW1wbGljaXQgSW1wb3J0IEluY2x1ZGUgSW5kdWN0aXZlIEluZml4IEluZm8gSW5pdGlhbCAnICtcbiAgICAgICAgJ0lubGluZSBJbnNwZWN0IEluc3RhbmNlIEluc3RhbmNlcyBJbnRybyBJbnRyb3MgSW52ZXJzaW9uIEludmVyc2lvbl9jbGVhciAnICtcbiAgICAgICAgJ0xhbmd1YWdlIExlZnQgTGVtbWEgTGV0IExpYnJhcmllcyBMaWJyYXJ5IExvYWQgTG9hZFBhdGggTG9jYWwgTG9jYXRlIEx0YWMgTUwgJyArXG4gICAgICAgICdNb2RlIE1vZHVsZSBNb2R1bGVzIE1vbm9tb3JwaGljIE1vcnBoaXNtIE5leHQgTm9JbmxpbmUgTm90YXRpb24gT2JsaWdhdGlvbiAnICtcbiAgICAgICAgJ09ibGlnYXRpb25zIE9wYXF1ZSBPcGVuIE9wdGltaXplIE9wdGlvbnMgUGFyYW1ldGVyIFBhcmFtZXRlcnMgUGFyYW1ldHJpYyAnICtcbiAgICAgICAgJ1BhdGggUGF0aHMgcGF0dGVybiBQb2x5bW9ycGhpYyBQcmV0ZXJtIFByaW50IFByaW50aW5nIFByb2dyYW0gUHJvamVjdGlvbnMgJyArXG4gICAgICAgICdQcm9vZiBQcm9wb3NpdGlvbiBQd2QgUWVkIFF1aXQgUmVjIFJlY29yZCBSZWN1cnNpdmUgUmVkaXJlY3QgUmVsYXRpb24gUmVtYXJrICcgK1xuICAgICAgICAnUmVtb3ZlIFJlcXVpcmUgUmVzZXJ2ZWQgUmVzZXQgUmVzb2x2ZSBSZXN0YXJ0IFJld3JpdGUgUmlnaHQgUmluZyBSaW5ncyBTYXZlICcgK1xuICAgICAgICAnU2NoZW1lIFNjb3BlIFNjb3BlcyBTY3JpcHQgU2VhcmNoIFNlYXJjaEFib3V0IFNlYXJjaEhlYWQgU2VhcmNoUGF0dGVybiAnICtcbiAgICAgICAgJ1NlYXJjaFJld3JpdGUgU2VjdGlvbiBTZXBhcmF0ZSBTZXQgU2V0b2lkIFNob3cgU29sdmUgU29ydGVkIFN0ZXAgU3RyYXRlZ2llcyAnICtcbiAgICAgICAgJ1N0cmF0ZWd5IFN0cnVjdHVyZSBTdWJDbGFzcyBUYWJsZSBUYWJsZXMgVGFjdGljIFRlcm0gVGVzdCBUaGVvcmVtIFRpbWUgJyArXG4gICAgICAgICdUaW1lb3V0IFRyYW5zcGFyZW50IFR5cGUgVHlwZWNsYXNzZXMgVHlwZXMgVW5kZWxpbWl0IFVuZG8gVW5mb2N1cyBVbmZvY3VzZWQgJyArXG4gICAgICAgICdVbmZvbGQgVW5pdmVyc2UgVW5pdmVyc2VzIFVuc2V0IFVuc2hlbHZlIHVzaW5nIFZhcmlhYmxlIFZhcmlhYmxlcyBWYXJpYW50ICcgK1xuICAgICAgICAnVmVyYm9zZSBWaXNpYmlsaXR5IHdoZXJlIHdpdGgnLFxuICAgICAgYnVpbHRfaW46XG4gICAgICAgICdhYnN0cmFjdCBhYnN1cmQgYWRtaXQgYWZ0ZXIgYXBwbHkgYXMgYXNzZXJ0IGFzc3VtcHRpb24gYXQgYXV0byBhdXRvcmV3cml0ZSAnICtcbiAgICAgICAgJ2F1dG91bmZvbGQgYmVmb3JlIGJvdHRvbSBidGF1dG8gYnkgY2FzZSBjYXNlX2VxIGNibiBjYnYgY2hhbmdlICcgK1xuICAgICAgICAnY2xhc3NpY2FsX2xlZnQgY2xhc3NpY2FsX3JpZ2h0IGNsZWFyIGNsZWFyYm9keSBjb2ZpeCBjb21wYXJlIGNvbXB1dGUgJyArXG4gICAgICAgICdjb25ncnVlbmNlIGNvbnN0cl9lcSBjb25zdHJ1Y3RvciBjb250cmFkaWN0IGNvbnRyYWRpY3Rpb24gY3V0IGN1dHJld3JpdGUgJyArXG4gICAgICAgICdjeWNsZSBkZWNpZGUgZGVjb21wb3NlIGRlcGVuZGVudCBkZXN0cnVjdCBkZXN0cnVjdGlvbiBkaW50dWl0aW9uICcgK1xuICAgICAgICAnZGlzY3JpbWluYXRlIGRpc2NyUiBkbyBkb3VibGUgZHRhdXRvIGVhcHBseSBlYXNzdW1wdGlvbiBlYXV0byBlY2FzZSAnICtcbiAgICAgICAgJ2Vjb25zdHJ1Y3RvciBlZGVzdHJ1Y3QgZWRpc2NyaW1pbmF0ZSBlZWxpbSBlZXhhY3QgZWV4aXN0cyBlaW5kdWN0aW9uICcgK1xuICAgICAgICAnZWluamVjdGlvbiBlbGVmdCBlbGltIGVsaW10eXBlIGVub3VnaCBlcXVhbGl0eSBlcmV3cml0ZSBlcmlnaHQgJyArXG4gICAgICAgICdlc2ltcGxpZnlfZXEgZXNwbGl0IGV2YXIgZXhhY3QgZXhhY3RseV9vbmNlIGV4ZmFsc28gZXhpc3RzIGZfZXF1YWwgZmFpbCAnICtcbiAgICAgICAgJ2ZpZWxkIGZpZWxkX3NpbXBsaWZ5IGZpZWxkX3NpbXBsaWZ5X2VxIGZpcnN0IGZpcnN0b3JkZXIgZml4IGZvbGQgZm91cmllciAnICtcbiAgICAgICAgJ2Z1bmN0aW9uYWwgZ2VuZXJhbGl6ZSBnZW5lcmFsaXppbmcgZ2ZhaWwgZ2l2ZV91cCBoYXNfZXZhciBobmYgaWR0YWMgaW4gJyArXG4gICAgICAgICdpbmR1Y3Rpb24gaW5qZWN0aW9uIGluc3RhbnRpYXRlIGludHJvIGludHJvX3BhdHRlcm4gaW50cm9zIGludHVpdGlvbiAnICtcbiAgICAgICAgJ2ludmVyc2lvbiBpbnZlcnNpb25fY2xlYXIgaXNfZXZhciBpc192YXIgbGFwcGx5IGxhenkgbGVmdCBsaWEgbHJhIG1vdmUgJyArXG4gICAgICAgICduYXRpdmVfY29tcHV0ZSBuaWEgbnNhdHogb21lZ2Egb25jZSBwYXR0ZXJuIHBvc2UgcHJvZ3Jlc3MgcHJvb2YgcHNhdHogcXVvdGUgJyArXG4gICAgICAgICdyZWNvcmQgcmVkIHJlZmluZSByZWZsZXhpdml0eSByZW1lbWJlciByZW5hbWUgcmVwZWF0IHJlcGxhY2UgcmV2ZXJ0ICcgK1xuICAgICAgICAncmV2Z29hbHMgcmV3cml0ZSByZXdyaXRlX3N0cmF0IHJpZ2h0IHJpbmcgcmluZ19zaW1wbGlmeSBydGF1dG8gc2V0ICcgK1xuICAgICAgICAnc2V0b2lkX3JlZmxleGl2aXR5IHNldG9pZF9yZXBsYWNlIHNldG9pZF9yZXdyaXRlIHNldG9pZF9zeW1tZXRyeSAnICtcbiAgICAgICAgJ3NldG9pZF90cmFuc2l0aXZpdHkgc2hlbHZlIHNoZWx2ZV91bmlmaWFibGUgc2ltcGwgc2ltcGxlIHNpbXBsaWZ5X2VxIHNvbHZlICcgK1xuICAgICAgICAnc3BlY2lhbGl6ZSBzcGxpdCBzcGxpdF9SYWJzIHNwbGl0X1JtdWx0IHN0ZXBsIHN0ZXByIHN1YnN0IHN1bSBzd2FwICcgK1xuICAgICAgICAnc3ltbWV0cnkgdGFjdGljIHRhdXRvIHRpbWUgdGltZW91dCB0b3AgdHJhbnNpdGl2aXR5IHRyaXZpYWwgdHJ5IHRyeWlmICcgK1xuICAgICAgICAndW5mb2xkIHVuaWZ5IHVudGlsIHVzaW5nIHZtX2NvbXB1dGUgd2l0aCdcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5DT01NRU5UKCdcXFxcKFxcXFwqJywgJ1xcXFwqXFxcXCknKSxcbiAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndHlwZScsXG4gICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgYmVnaW46ICdcXFxcfFxcXFxzKicsXG4gICAgICAgIGVuZDogJ1xcXFx3KydcbiAgICAgIH0sXG4gICAgICB7IC8vIHJlbGV2YW5jZSBib29zdGVyXG4gICAgICAgIGJlZ2luOiAvWy09XT4vXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGNvcTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==