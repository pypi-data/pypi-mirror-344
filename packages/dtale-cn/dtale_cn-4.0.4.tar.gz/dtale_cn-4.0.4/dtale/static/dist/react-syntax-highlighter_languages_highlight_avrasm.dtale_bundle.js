(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_avrasm"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/avrasm.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/avrasm.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: AVR Assembly
Author: Vladimir Ermakov <vooon341@gmail.com>
Category: assembler
Website: https://www.microchip.com/webdoc/avrassembler/avrassembler.wb_instruction_list.html
*/

/** @type LanguageFn */
function avrasm(hljs) {
  return {
    name: 'AVR Assembly',
    case_insensitive: true,
    keywords: {
      $pattern: '\\.?' + hljs.IDENT_RE,
      keyword:
        /* mnemonic */
        'adc add adiw and andi asr bclr bld brbc brbs brcc brcs break breq brge brhc brhs ' +
        'brid brie brlo brlt brmi brne brpl brsh brtc brts brvc brvs bset bst call cbi cbr ' +
        'clc clh cli cln clr cls clt clv clz com cp cpc cpi cpse dec eicall eijmp elpm eor ' +
        'fmul fmuls fmulsu icall ijmp in inc jmp ld ldd ldi lds lpm lsl lsr mov movw mul ' +
        'muls mulsu neg nop or ori out pop push rcall ret reti rjmp rol ror sbc sbr sbrc sbrs ' +
        'sec seh sbi sbci sbic sbis sbiw sei sen ser ses set sev sez sleep spm st std sts sub ' +
        'subi swap tst wdr',
      built_in:
        /* general purpose registers */
        'r0 r1 r2 r3 r4 r5 r6 r7 r8 r9 r10 r11 r12 r13 r14 r15 r16 r17 r18 r19 r20 r21 r22 ' +
        'r23 r24 r25 r26 r27 r28 r29 r30 r31 x|0 xh xl y|0 yh yl z|0 zh zl ' +
        /* IO Registers (ATMega128) */
        'ucsr1c udr1 ucsr1a ucsr1b ubrr1l ubrr1h ucsr0c ubrr0h tccr3c tccr3a tccr3b tcnt3h ' +
        'tcnt3l ocr3ah ocr3al ocr3bh ocr3bl ocr3ch ocr3cl icr3h icr3l etimsk etifr tccr1c ' +
        'ocr1ch ocr1cl twcr twdr twar twsr twbr osccal xmcra xmcrb eicra spmcsr spmcr portg ' +
        'ddrg ping portf ddrf sreg sph spl xdiv rampz eicrb eimsk gimsk gicr eifr gifr timsk ' +
        'tifr mcucr mcucsr tccr0 tcnt0 ocr0 assr tccr1a tccr1b tcnt1h tcnt1l ocr1ah ocr1al ' +
        'ocr1bh ocr1bl icr1h icr1l tccr2 tcnt2 ocr2 ocdr wdtcr sfior eearh eearl eedr eecr ' +
        'porta ddra pina portb ddrb pinb portc ddrc pinc portd ddrd pind spdr spsr spcr udr0 ' +
        'ucsr0a ucsr0b ubrr0l acsr admux adcsr adch adcl porte ddre pine pinf',
      meta:
        '.byte .cseg .db .def .device .dseg .dw .endmacro .equ .eseg .exit .include .list ' +
        '.listmac .macro .nolist .org .set'
    },
    contains: [
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.COMMENT(
        ';',
        '$',
        {
          relevance: 0
        }
      ),
      hljs.C_NUMBER_MODE, // 0x..., decimal, float
      hljs.BINARY_NUMBER_MODE, // 0b...
      {
        className: 'number',
        begin: '\\b(\\$[a-zA-Z0-9]+|0o[0-7]+)' // $..., 0o...
      },
      hljs.QUOTE_STRING_MODE,
      {
        className: 'string',
        begin: '\'',
        end: '[^\\\\]\'',
        illegal: '[^\\\\][^\']'
      },
      {
        className: 'symbol',
        begin: '^[A-Za-z0-9_.$]+:'
      },
      {
        className: 'meta',
        begin: '#',
        end: '$'
      },
      { // substitution within a macro
        className: 'subst',
        begin: '@[0-9]+'
      }
    ]
  };
}

module.exports = avrasm;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYXZyYXNtLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBLFVBQVU7QUFDVjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQLFFBQVE7QUFDUjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2F2cmFzbS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IEFWUiBBc3NlbWJseVxuQXV0aG9yOiBWbGFkaW1pciBFcm1ha292IDx2b29vbjM0MUBnbWFpbC5jb20+XG5DYXRlZ29yeTogYXNzZW1ibGVyXG5XZWJzaXRlOiBodHRwczovL3d3dy5taWNyb2NoaXAuY29tL3dlYmRvYy9hdnJhc3NlbWJsZXIvYXZyYXNzZW1ibGVyLndiX2luc3RydWN0aW9uX2xpc3QuaHRtbFxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGF2cmFzbShobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0FWUiBBc3NlbWJseScsXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAgJHBhdHRlcm46ICdcXFxcLj8nICsgaGxqcy5JREVOVF9SRSxcbiAgICAgIGtleXdvcmQ6XG4gICAgICAgIC8qIG1uZW1vbmljICovXG4gICAgICAgICdhZGMgYWRkIGFkaXcgYW5kIGFuZGkgYXNyIGJjbHIgYmxkIGJyYmMgYnJicyBicmNjIGJyY3MgYnJlYWsgYnJlcSBicmdlIGJyaGMgYnJocyAnICtcbiAgICAgICAgJ2JyaWQgYnJpZSBicmxvIGJybHQgYnJtaSBicm5lIGJycGwgYnJzaCBicnRjIGJydHMgYnJ2YyBicnZzIGJzZXQgYnN0IGNhbGwgY2JpIGNiciAnICtcbiAgICAgICAgJ2NsYyBjbGggY2xpIGNsbiBjbHIgY2xzIGNsdCBjbHYgY2x6IGNvbSBjcCBjcGMgY3BpIGNwc2UgZGVjIGVpY2FsbCBlaWptcCBlbHBtIGVvciAnICtcbiAgICAgICAgJ2ZtdWwgZm11bHMgZm11bHN1IGljYWxsIGlqbXAgaW4gaW5jIGptcCBsZCBsZGQgbGRpIGxkcyBscG0gbHNsIGxzciBtb3YgbW92dyBtdWwgJyArXG4gICAgICAgICdtdWxzIG11bHN1IG5lZyBub3Agb3Igb3JpIG91dCBwb3AgcHVzaCByY2FsbCByZXQgcmV0aSByam1wIHJvbCByb3Igc2JjIHNiciBzYnJjIHNicnMgJyArXG4gICAgICAgICdzZWMgc2VoIHNiaSBzYmNpIHNiaWMgc2JpcyBzYml3IHNlaSBzZW4gc2VyIHNlcyBzZXQgc2V2IHNleiBzbGVlcCBzcG0gc3Qgc3RkIHN0cyBzdWIgJyArXG4gICAgICAgICdzdWJpIHN3YXAgdHN0IHdkcicsXG4gICAgICBidWlsdF9pbjpcbiAgICAgICAgLyogZ2VuZXJhbCBwdXJwb3NlIHJlZ2lzdGVycyAqL1xuICAgICAgICAncjAgcjEgcjIgcjMgcjQgcjUgcjYgcjcgcjggcjkgcjEwIHIxMSByMTIgcjEzIHIxNCByMTUgcjE2IHIxNyByMTggcjE5IHIyMCByMjEgcjIyICcgK1xuICAgICAgICAncjIzIHIyNCByMjUgcjI2IHIyNyByMjggcjI5IHIzMCByMzEgeHwwIHhoIHhsIHl8MCB5aCB5bCB6fDAgemggemwgJyArXG4gICAgICAgIC8qIElPIFJlZ2lzdGVycyAoQVRNZWdhMTI4KSAqL1xuICAgICAgICAndWNzcjFjIHVkcjEgdWNzcjFhIHVjc3IxYiB1YnJyMWwgdWJycjFoIHVjc3IwYyB1YnJyMGggdGNjcjNjIHRjY3IzYSB0Y2NyM2IgdGNudDNoICcgK1xuICAgICAgICAndGNudDNsIG9jcjNhaCBvY3IzYWwgb2NyM2JoIG9jcjNibCBvY3IzY2ggb2NyM2NsIGljcjNoIGljcjNsIGV0aW1zayBldGlmciB0Y2NyMWMgJyArXG4gICAgICAgICdvY3IxY2ggb2NyMWNsIHR3Y3IgdHdkciB0d2FyIHR3c3IgdHdiciBvc2NjYWwgeG1jcmEgeG1jcmIgZWljcmEgc3BtY3NyIHNwbWNyIHBvcnRnICcgK1xuICAgICAgICAnZGRyZyBwaW5nIHBvcnRmIGRkcmYgc3JlZyBzcGggc3BsIHhkaXYgcmFtcHogZWljcmIgZWltc2sgZ2ltc2sgZ2ljciBlaWZyIGdpZnIgdGltc2sgJyArXG4gICAgICAgICd0aWZyIG1jdWNyIG1jdWNzciB0Y2NyMCB0Y250MCBvY3IwIGFzc3IgdGNjcjFhIHRjY3IxYiB0Y250MWggdGNudDFsIG9jcjFhaCBvY3IxYWwgJyArXG4gICAgICAgICdvY3IxYmggb2NyMWJsIGljcjFoIGljcjFsIHRjY3IyIHRjbnQyIG9jcjIgb2NkciB3ZHRjciBzZmlvciBlZWFyaCBlZWFybCBlZWRyIGVlY3IgJyArXG4gICAgICAgICdwb3J0YSBkZHJhIHBpbmEgcG9ydGIgZGRyYiBwaW5iIHBvcnRjIGRkcmMgcGluYyBwb3J0ZCBkZHJkIHBpbmQgc3BkciBzcHNyIHNwY3IgdWRyMCAnICtcbiAgICAgICAgJ3Vjc3IwYSB1Y3NyMGIgdWJycjBsIGFjc3IgYWRtdXggYWRjc3IgYWRjaCBhZGNsIHBvcnRlIGRkcmUgcGluZSBwaW5mJyxcbiAgICAgIG1ldGE6XG4gICAgICAgICcuYnl0ZSAuY3NlZyAuZGIgLmRlZiAuZGV2aWNlIC5kc2VnIC5kdyAuZW5kbWFjcm8gLmVxdSAuZXNlZyAuZXhpdCAuaW5jbHVkZSAubGlzdCAnICtcbiAgICAgICAgJy5saXN0bWFjIC5tYWNybyAubm9saXN0IC5vcmcgLnNldCdcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DT01NRU5UKFxuICAgICAgICAnOycsXG4gICAgICAgICckJyxcbiAgICAgICAge1xuICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICB9XG4gICAgICApLFxuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLCAvLyAweC4uLiwgZGVjaW1hbCwgZmxvYXRcbiAgICAgIGhsanMuQklOQVJZX05VTUJFUl9NT0RFLCAvLyAwYi4uLlxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgICAgICBiZWdpbjogJ1xcXFxiKFxcXFwkW2EtekEtWjAtOV0rfDBvWzAtN10rKScgLy8gJC4uLiwgMG8uLi5cbiAgICAgIH0sXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogJ1xcJycsXG4gICAgICAgIGVuZDogJ1teXFxcXFxcXFxdXFwnJyxcbiAgICAgICAgaWxsZWdhbDogJ1teXFxcXFxcXFxdW15cXCddJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICAgICAgYmVnaW46ICdeW0EtWmEtejAtOV8uJF0rOidcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogJyMnLFxuICAgICAgICBlbmQ6ICckJ1xuICAgICAgfSxcbiAgICAgIHsgLy8gc3Vic3RpdHV0aW9uIHdpdGhpbiBhIG1hY3JvXG4gICAgICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICAgICAgYmVnaW46ICdAWzAtOV0rJ1xuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBhdnJhc207XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=