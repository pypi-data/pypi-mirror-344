(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_hsp"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/hsp.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/hsp.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: HSP
Author: prince <MC.prince.0203@gmail.com>
Website: https://en.wikipedia.org/wiki/Hot_Soup_Processor
Category: scripting
*/

function hsp(hljs) {
  return {
    name: 'HSP',
    case_insensitive: true,
    keywords: {
      $pattern: /[\w._]+/,
      keyword: 'goto gosub return break repeat loop continue wait await dim sdim foreach dimtype dup dupptr end stop newmod delmod mref run exgoto on mcall assert logmes newlab resume yield onexit onerror onkey onclick oncmd exist delete mkdir chdir dirlist bload bsave bcopy memfile if else poke wpoke lpoke getstr chdpm memexpand memcpy memset notesel noteadd notedel noteload notesave randomize noteunsel noteget split strrep setease button chgdisp exec dialog mmload mmplay mmstop mci pset pget syscolor mes print title pos circle cls font sysfont objsize picload color palcolor palette redraw width gsel gcopy gzoom gmode bmpsave hsvcolor getkey listbox chkbox combox input mesbox buffer screen bgscr mouse objsel groll line clrobj boxf objprm objmode stick grect grotate gsquare gradf objimage objskip objenable celload celdiv celput newcom querycom delcom cnvstow comres axobj winobj sendmsg comevent comevarg sarrayconv callfunc cnvwtos comevdisp libptr system hspstat hspver stat cnt err strsize looplev sublev iparam wparam lparam refstr refdval int rnd strlen length length2 length3 length4 vartype gettime peek wpeek lpeek varptr varuse noteinfo instr abs limit getease str strmid strf getpath strtrim sin cos tan atan sqrt double absf expf logf limitf powf geteasef mousex mousey mousew hwnd hinstance hdc ginfo objinfo dirinfo sysinfo thismod __hspver__ __hsp30__ __date__ __time__ __line__ __file__ _debug __hspdef__ and or xor not screen_normal screen_palette screen_hide screen_fixedsize screen_tool screen_frame gmode_gdi gmode_mem gmode_rgb0 gmode_alpha gmode_rgb0alpha gmode_add gmode_sub gmode_pixela ginfo_mx ginfo_my ginfo_act ginfo_sel ginfo_wx1 ginfo_wy1 ginfo_wx2 ginfo_wy2 ginfo_vx ginfo_vy ginfo_sizex ginfo_sizey ginfo_winx ginfo_winy ginfo_mesx ginfo_mesy ginfo_r ginfo_g ginfo_b ginfo_paluse ginfo_dispx ginfo_dispy ginfo_cx ginfo_cy ginfo_intid ginfo_newid ginfo_sx ginfo_sy objinfo_mode objinfo_bmscr objinfo_hwnd notemax notesize dir_cur dir_exe dir_win dir_sys dir_cmdline dir_desktop dir_mydoc dir_tv font_normal font_bold font_italic font_underline font_strikeout font_antialias objmode_normal objmode_guifont objmode_usefont gsquare_grad msgothic msmincho do until while wend for next _break _continue switch case default swbreak swend ddim ldim alloc m_pi rad2deg deg2rad ease_linear ease_quad_in ease_quad_out ease_quad_inout ease_cubic_in ease_cubic_out ease_cubic_inout ease_quartic_in ease_quartic_out ease_quartic_inout ease_bounce_in ease_bounce_out ease_bounce_inout ease_shake_in ease_shake_out ease_shake_inout ease_loop'
    },
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.APOS_STRING_MODE,

      {
        // multi-line string
        className: 'string',
        begin: /\{"/,
        end: /"\}/,
        contains: [hljs.BACKSLASH_ESCAPE]
      },

      hljs.COMMENT(';', '$', {
        relevance: 0
      }),

      {
        // pre-processor
        className: 'meta',
        begin: '#',
        end: '$',
        keywords: {
          'meta-keyword': 'addion cfunc cmd cmpopt comfunc const defcfunc deffunc define else endif enum epack func global if ifdef ifndef include modcfunc modfunc modinit modterm module pack packopt regcmd runtime undef usecom uselib'
        },
        contains: [
          hljs.inherit(hljs.QUOTE_STRING_MODE, {
            className: 'meta-string'
          }),
          hljs.NUMBER_MODE,
          hljs.C_NUMBER_MODE,
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE
        ]
      },

      {
        // label
        className: 'symbol',
        begin: '^\\*(\\w+|@)'
      },

      hljs.NUMBER_MODE,
      hljs.C_NUMBER_MODE
    ]
  };
}

module.exports = hsp;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfaHNwLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQjtBQUNsQixpQkFBaUI7QUFDakI7QUFDQSxPQUFPOztBQUVQLHFCQUFxQjtBQUNyQjtBQUNBLE9BQU87O0FBRVA7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPOztBQUVQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTzs7QUFFUDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9oc3AuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBIU1BcbkF1dGhvcjogcHJpbmNlIDxNQy5wcmluY2UuMDIwM0BnbWFpbC5jb20+XG5XZWJzaXRlOiBodHRwczovL2VuLndpa2lwZWRpYS5vcmcvd2lraS9Ib3RfU291cF9Qcm9jZXNzb3JcbkNhdGVnb3J5OiBzY3JpcHRpbmdcbiovXG5cbmZ1bmN0aW9uIGhzcChobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0hTUCcsXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAgJHBhdHRlcm46IC9bXFx3Ll9dKy8sXG4gICAgICBrZXl3b3JkOiAnZ290byBnb3N1YiByZXR1cm4gYnJlYWsgcmVwZWF0IGxvb3AgY29udGludWUgd2FpdCBhd2FpdCBkaW0gc2RpbSBmb3JlYWNoIGRpbXR5cGUgZHVwIGR1cHB0ciBlbmQgc3RvcCBuZXdtb2QgZGVsbW9kIG1yZWYgcnVuIGV4Z290byBvbiBtY2FsbCBhc3NlcnQgbG9nbWVzIG5ld2xhYiByZXN1bWUgeWllbGQgb25leGl0IG9uZXJyb3Igb25rZXkgb25jbGljayBvbmNtZCBleGlzdCBkZWxldGUgbWtkaXIgY2hkaXIgZGlybGlzdCBibG9hZCBic2F2ZSBiY29weSBtZW1maWxlIGlmIGVsc2UgcG9rZSB3cG9rZSBscG9rZSBnZXRzdHIgY2hkcG0gbWVtZXhwYW5kIG1lbWNweSBtZW1zZXQgbm90ZXNlbCBub3RlYWRkIG5vdGVkZWwgbm90ZWxvYWQgbm90ZXNhdmUgcmFuZG9taXplIG5vdGV1bnNlbCBub3RlZ2V0IHNwbGl0IHN0cnJlcCBzZXRlYXNlIGJ1dHRvbiBjaGdkaXNwIGV4ZWMgZGlhbG9nIG1tbG9hZCBtbXBsYXkgbW1zdG9wIG1jaSBwc2V0IHBnZXQgc3lzY29sb3IgbWVzIHByaW50IHRpdGxlIHBvcyBjaXJjbGUgY2xzIGZvbnQgc3lzZm9udCBvYmpzaXplIHBpY2xvYWQgY29sb3IgcGFsY29sb3IgcGFsZXR0ZSByZWRyYXcgd2lkdGggZ3NlbCBnY29weSBnem9vbSBnbW9kZSBibXBzYXZlIGhzdmNvbG9yIGdldGtleSBsaXN0Ym94IGNoa2JveCBjb21ib3ggaW5wdXQgbWVzYm94IGJ1ZmZlciBzY3JlZW4gYmdzY3IgbW91c2Ugb2Jqc2VsIGdyb2xsIGxpbmUgY2xyb2JqIGJveGYgb2JqcHJtIG9iam1vZGUgc3RpY2sgZ3JlY3QgZ3JvdGF0ZSBnc3F1YXJlIGdyYWRmIG9iamltYWdlIG9ianNraXAgb2JqZW5hYmxlIGNlbGxvYWQgY2VsZGl2IGNlbHB1dCBuZXdjb20gcXVlcnljb20gZGVsY29tIGNudnN0b3cgY29tcmVzIGF4b2JqIHdpbm9iaiBzZW5kbXNnIGNvbWV2ZW50IGNvbWV2YXJnIHNhcnJheWNvbnYgY2FsbGZ1bmMgY252d3RvcyBjb21ldmRpc3AgbGlicHRyIHN5c3RlbSBoc3BzdGF0IGhzcHZlciBzdGF0IGNudCBlcnIgc3Ryc2l6ZSBsb29wbGV2IHN1YmxldiBpcGFyYW0gd3BhcmFtIGxwYXJhbSByZWZzdHIgcmVmZHZhbCBpbnQgcm5kIHN0cmxlbiBsZW5ndGggbGVuZ3RoMiBsZW5ndGgzIGxlbmd0aDQgdmFydHlwZSBnZXR0aW1lIHBlZWsgd3BlZWsgbHBlZWsgdmFycHRyIHZhcnVzZSBub3RlaW5mbyBpbnN0ciBhYnMgbGltaXQgZ2V0ZWFzZSBzdHIgc3RybWlkIHN0cmYgZ2V0cGF0aCBzdHJ0cmltIHNpbiBjb3MgdGFuIGF0YW4gc3FydCBkb3VibGUgYWJzZiBleHBmIGxvZ2YgbGltaXRmIHBvd2YgZ2V0ZWFzZWYgbW91c2V4IG1vdXNleSBtb3VzZXcgaHduZCBoaW5zdGFuY2UgaGRjIGdpbmZvIG9iamluZm8gZGlyaW5mbyBzeXNpbmZvIHRoaXNtb2QgX19oc3B2ZXJfXyBfX2hzcDMwX18gX19kYXRlX18gX190aW1lX18gX19saW5lX18gX19maWxlX18gX2RlYnVnIF9faHNwZGVmX18gYW5kIG9yIHhvciBub3Qgc2NyZWVuX25vcm1hbCBzY3JlZW5fcGFsZXR0ZSBzY3JlZW5faGlkZSBzY3JlZW5fZml4ZWRzaXplIHNjcmVlbl90b29sIHNjcmVlbl9mcmFtZSBnbW9kZV9nZGkgZ21vZGVfbWVtIGdtb2RlX3JnYjAgZ21vZGVfYWxwaGEgZ21vZGVfcmdiMGFscGhhIGdtb2RlX2FkZCBnbW9kZV9zdWIgZ21vZGVfcGl4ZWxhIGdpbmZvX214IGdpbmZvX215IGdpbmZvX2FjdCBnaW5mb19zZWwgZ2luZm9fd3gxIGdpbmZvX3d5MSBnaW5mb193eDIgZ2luZm9fd3kyIGdpbmZvX3Z4IGdpbmZvX3Z5IGdpbmZvX3NpemV4IGdpbmZvX3NpemV5IGdpbmZvX3dpbnggZ2luZm9fd2lueSBnaW5mb19tZXN4IGdpbmZvX21lc3kgZ2luZm9fciBnaW5mb19nIGdpbmZvX2IgZ2luZm9fcGFsdXNlIGdpbmZvX2Rpc3B4IGdpbmZvX2Rpc3B5IGdpbmZvX2N4IGdpbmZvX2N5IGdpbmZvX2ludGlkIGdpbmZvX25ld2lkIGdpbmZvX3N4IGdpbmZvX3N5IG9iamluZm9fbW9kZSBvYmppbmZvX2Jtc2NyIG9iamluZm9faHduZCBub3RlbWF4IG5vdGVzaXplIGRpcl9jdXIgZGlyX2V4ZSBkaXJfd2luIGRpcl9zeXMgZGlyX2NtZGxpbmUgZGlyX2Rlc2t0b3AgZGlyX215ZG9jIGRpcl90diBmb250X25vcm1hbCBmb250X2JvbGQgZm9udF9pdGFsaWMgZm9udF91bmRlcmxpbmUgZm9udF9zdHJpa2VvdXQgZm9udF9hbnRpYWxpYXMgb2JqbW9kZV9ub3JtYWwgb2JqbW9kZV9ndWlmb250IG9iam1vZGVfdXNlZm9udCBnc3F1YXJlX2dyYWQgbXNnb3RoaWMgbXNtaW5jaG8gZG8gdW50aWwgd2hpbGUgd2VuZCBmb3IgbmV4dCBfYnJlYWsgX2NvbnRpbnVlIHN3aXRjaCBjYXNlIGRlZmF1bHQgc3dicmVhayBzd2VuZCBkZGltIGxkaW0gYWxsb2MgbV9waSByYWQyZGVnIGRlZzJyYWQgZWFzZV9saW5lYXIgZWFzZV9xdWFkX2luIGVhc2VfcXVhZF9vdXQgZWFzZV9xdWFkX2lub3V0IGVhc2VfY3ViaWNfaW4gZWFzZV9jdWJpY19vdXQgZWFzZV9jdWJpY19pbm91dCBlYXNlX3F1YXJ0aWNfaW4gZWFzZV9xdWFydGljX291dCBlYXNlX3F1YXJ0aWNfaW5vdXQgZWFzZV9ib3VuY2VfaW4gZWFzZV9ib3VuY2Vfb3V0IGVhc2VfYm91bmNlX2lub3V0IGVhc2Vfc2hha2VfaW4gZWFzZV9zaGFrZV9vdXQgZWFzZV9zaGFrZV9pbm91dCBlYXNlX2xvb3AnXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG5cbiAgICAgIHtcbiAgICAgICAgLy8gbXVsdGktbGluZSBzdHJpbmdcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgYmVnaW46IC9cXHtcIi8sXG4gICAgICAgIGVuZDogL1wiXFx9LyxcbiAgICAgICAgY29udGFpbnM6IFtobGpzLkJBQ0tTTEFTSF9FU0NBUEVdXG4gICAgICB9LFxuXG4gICAgICBobGpzLkNPTU1FTlQoJzsnLCAnJCcsIHtcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9KSxcblxuICAgICAge1xuICAgICAgICAvLyBwcmUtcHJvY2Vzc29yXG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogJyMnLFxuICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAga2V5d29yZHM6IHtcbiAgICAgICAgICAnbWV0YS1rZXl3b3JkJzogJ2FkZGlvbiBjZnVuYyBjbWQgY21wb3B0IGNvbWZ1bmMgY29uc3QgZGVmY2Z1bmMgZGVmZnVuYyBkZWZpbmUgZWxzZSBlbmRpZiBlbnVtIGVwYWNrIGZ1bmMgZ2xvYmFsIGlmIGlmZGVmIGlmbmRlZiBpbmNsdWRlIG1vZGNmdW5jIG1vZGZ1bmMgbW9kaW5pdCBtb2R0ZXJtIG1vZHVsZSBwYWNrIHBhY2tvcHQgcmVnY21kIHJ1bnRpbWUgdW5kZWYgdXNlY29tIHVzZWxpYidcbiAgICAgICAgfSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBobGpzLmluaGVyaXQoaGxqcy5RVU9URV9TVFJJTkdfTU9ERSwge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnbWV0YS1zdHJpbmcnXG4gICAgICAgICAgfSksXG4gICAgICAgICAgaGxqcy5OVU1CRVJfTU9ERSxcbiAgICAgICAgICBobGpzLkNfTlVNQkVSX01PREUsXG4gICAgICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcblxuICAgICAge1xuICAgICAgICAvLyBsYWJlbFxuICAgICAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgICAgICBiZWdpbjogJ15cXFxcKihcXFxcdyt8QCknXG4gICAgICB9LFxuXG4gICAgICBobGpzLk5VTUJFUl9NT0RFLFxuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGhzcDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==