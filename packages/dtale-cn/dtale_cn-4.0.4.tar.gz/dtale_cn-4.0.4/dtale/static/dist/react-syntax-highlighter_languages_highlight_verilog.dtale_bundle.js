(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_verilog"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/verilog.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/verilog.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
Language: Verilog
Author: Jon Evans <jon@craftyjon.com>
Contributors: Boone Severson <boone.severson@gmail.com>
Description: Verilog is a hardware description language used in electronic design automation to describe digital and mixed-signal systems. This highlighter supports Verilog and SystemVerilog through IEEE 1800-2012.
Website: http://www.verilog.com
*/

function verilog(hljs) {
  const SV_KEYWORDS = {
    $pattern: /[\w\$]+/,
    keyword:
      'accept_on alias always always_comb always_ff always_latch and assert assign ' +
      'assume automatic before begin bind bins binsof bit break buf|0 bufif0 bufif1 ' +
      'byte case casex casez cell chandle checker class clocking cmos config const ' +
      'constraint context continue cover covergroup coverpoint cross deassign default ' +
      'defparam design disable dist do edge else end endcase endchecker endclass ' +
      'endclocking endconfig endfunction endgenerate endgroup endinterface endmodule ' +
      'endpackage endprimitive endprogram endproperty endspecify endsequence endtable ' +
      'endtask enum event eventually expect export extends extern final first_match for ' +
      'force foreach forever fork forkjoin function generate|5 genvar global highz0 highz1 ' +
      'if iff ifnone ignore_bins illegal_bins implements implies import incdir include ' +
      'initial inout input inside instance int integer interconnect interface intersect ' +
      'join join_any join_none large let liblist library local localparam logic longint ' +
      'macromodule matches medium modport module nand negedge nettype new nexttime nmos ' +
      'nor noshowcancelled not notif0 notif1 or output package packed parameter pmos ' +
      'posedge primitive priority program property protected pull0 pull1 pulldown pullup ' +
      'pulsestyle_ondetect pulsestyle_onevent pure rand randc randcase randsequence rcmos ' +
      'real realtime ref reg reject_on release repeat restrict return rnmos rpmos rtran ' +
      'rtranif0 rtranif1 s_always s_eventually s_nexttime s_until s_until_with scalared ' +
      'sequence shortint shortreal showcancelled signed small soft solve specify specparam ' +
      'static string strong strong0 strong1 struct super supply0 supply1 sync_accept_on ' +
      'sync_reject_on table tagged task this throughout time timeprecision timeunit tran ' +
      'tranif0 tranif1 tri tri0 tri1 triand trior trireg type typedef union unique unique0 ' +
      'unsigned until until_with untyped use uwire var vectored virtual void wait wait_order ' +
      'wand weak weak0 weak1 while wildcard wire with within wor xnor xor',
    literal:
      'null',
    built_in:
      '$finish $stop $exit $fatal $error $warning $info $realtime $time $printtimescale ' +
      '$bitstoreal $bitstoshortreal $itor $signed $cast $bits $stime $timeformat ' +
      '$realtobits $shortrealtobits $rtoi $unsigned $asserton $assertkill $assertpasson ' +
      '$assertfailon $assertnonvacuouson $assertoff $assertcontrol $assertpassoff ' +
      '$assertfailoff $assertvacuousoff $isunbounded $sampled $fell $changed $past_gclk ' +
      '$fell_gclk $changed_gclk $rising_gclk $steady_gclk $coverage_control ' +
      '$coverage_get $coverage_save $set_coverage_db_name $rose $stable $past ' +
      '$rose_gclk $stable_gclk $future_gclk $falling_gclk $changing_gclk $display ' +
      '$coverage_get_max $coverage_merge $get_coverage $load_coverage_db $typename ' +
      '$unpacked_dimensions $left $low $increment $clog2 $ln $log10 $exp $sqrt $pow ' +
      '$floor $ceil $sin $cos $tan $countbits $onehot $isunknown $fatal $warning ' +
      '$dimensions $right $high $size $asin $acos $atan $atan2 $hypot $sinh $cosh ' +
      '$tanh $asinh $acosh $atanh $countones $onehot0 $error $info $random ' +
      '$dist_chi_square $dist_erlang $dist_exponential $dist_normal $dist_poisson ' +
      '$dist_t $dist_uniform $q_initialize $q_remove $q_exam $async$and$array ' +
      '$async$nand$array $async$or$array $async$nor$array $sync$and$array ' +
      '$sync$nand$array $sync$or$array $sync$nor$array $q_add $q_full $psprintf ' +
      '$async$and$plane $async$nand$plane $async$or$plane $async$nor$plane ' +
      '$sync$and$plane $sync$nand$plane $sync$or$plane $sync$nor$plane $system ' +
      '$display $displayb $displayh $displayo $strobe $strobeb $strobeh $strobeo ' +
      '$write $readmemb $readmemh $writememh $value$plusargs ' +
      '$dumpvars $dumpon $dumplimit $dumpports $dumpportson $dumpportslimit ' +
      '$writeb $writeh $writeo $monitor $monitorb $monitorh $monitoro $writememb ' +
      '$dumpfile $dumpoff $dumpall $dumpflush $dumpportsoff $dumpportsall ' +
      '$dumpportsflush $fclose $fdisplay $fdisplayb $fdisplayh $fdisplayo ' +
      '$fstrobe $fstrobeb $fstrobeh $fstrobeo $swrite $swriteb $swriteh ' +
      '$swriteo $fscanf $fread $fseek $fflush $feof $fopen $fwrite $fwriteb ' +
      '$fwriteh $fwriteo $fmonitor $fmonitorb $fmonitorh $fmonitoro $sformat ' +
      '$sformatf $fgetc $ungetc $fgets $sscanf $rewind $ftell $ferror'
  };

  return {
    name: 'Verilog',
    aliases: [
      'v',
      'sv',
      'svh'
    ],
    case_insensitive: false,
    keywords: SV_KEYWORDS,
    contains: [
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.C_LINE_COMMENT_MODE,
      hljs.QUOTE_STRING_MODE,
      {
        className: 'number',
        contains: [ hljs.BACKSLASH_ESCAPE ],
        variants: [
          {
            begin: '\\b((\\d+\'(b|h|o|d|B|H|O|D))[0-9xzXZa-fA-F_]+)'
          },
          {
            begin: '\\B((\'(b|h|o|d|B|H|O|D))[0-9xzXZa-fA-F_]+)'
          },
          {
            begin: '\\b([0-9_])+',
            relevance: 0
          }
        ]
      },
      /* parameters to instances */
      {
        className: 'variable',
        variants: [
          {
            begin: '#\\((?!parameter).+\\)'
          },
          {
            begin: '\\.\\w+',
            relevance: 0
          }
        ]
      },
      {
        className: 'meta',
        begin: '`',
        end: '$',
        keywords: {
          'meta-keyword':
            'define __FILE__ ' +
            '__LINE__ begin_keywords celldefine default_nettype define ' +
            'else elsif end_keywords endcelldefine endif ifdef ifndef ' +
            'include line nounconnected_drive pragma resetall timescale ' +
            'unconnected_drive undef undefineall'
        },
        relevance: 0
      }
    ]
  };
}

module.exports = verilog;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfdmVyaWxvZy5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy92ZXJpbG9nLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogVmVyaWxvZ1xuQXV0aG9yOiBKb24gRXZhbnMgPGpvbkBjcmFmdHlqb24uY29tPlxuQ29udHJpYnV0b3JzOiBCb29uZSBTZXZlcnNvbiA8Ym9vbmUuc2V2ZXJzb25AZ21haWwuY29tPlxuRGVzY3JpcHRpb246IFZlcmlsb2cgaXMgYSBoYXJkd2FyZSBkZXNjcmlwdGlvbiBsYW5ndWFnZSB1c2VkIGluIGVsZWN0cm9uaWMgZGVzaWduIGF1dG9tYXRpb24gdG8gZGVzY3JpYmUgZGlnaXRhbCBhbmQgbWl4ZWQtc2lnbmFsIHN5c3RlbXMuIFRoaXMgaGlnaGxpZ2h0ZXIgc3VwcG9ydHMgVmVyaWxvZyBhbmQgU3lzdGVtVmVyaWxvZyB0aHJvdWdoIElFRUUgMTgwMC0yMDEyLlxuV2Vic2l0ZTogaHR0cDovL3d3dy52ZXJpbG9nLmNvbVxuKi9cblxuZnVuY3Rpb24gdmVyaWxvZyhobGpzKSB7XG4gIGNvbnN0IFNWX0tFWVdPUkRTID0ge1xuICAgICRwYXR0ZXJuOiAvW1xcd1xcJF0rLyxcbiAgICBrZXl3b3JkOlxuICAgICAgJ2FjY2VwdF9vbiBhbGlhcyBhbHdheXMgYWx3YXlzX2NvbWIgYWx3YXlzX2ZmIGFsd2F5c19sYXRjaCBhbmQgYXNzZXJ0IGFzc2lnbiAnICtcbiAgICAgICdhc3N1bWUgYXV0b21hdGljIGJlZm9yZSBiZWdpbiBiaW5kIGJpbnMgYmluc29mIGJpdCBicmVhayBidWZ8MCBidWZpZjAgYnVmaWYxICcgK1xuICAgICAgJ2J5dGUgY2FzZSBjYXNleCBjYXNleiBjZWxsIGNoYW5kbGUgY2hlY2tlciBjbGFzcyBjbG9ja2luZyBjbW9zIGNvbmZpZyBjb25zdCAnICtcbiAgICAgICdjb25zdHJhaW50IGNvbnRleHQgY29udGludWUgY292ZXIgY292ZXJncm91cCBjb3ZlcnBvaW50IGNyb3NzIGRlYXNzaWduIGRlZmF1bHQgJyArXG4gICAgICAnZGVmcGFyYW0gZGVzaWduIGRpc2FibGUgZGlzdCBkbyBlZGdlIGVsc2UgZW5kIGVuZGNhc2UgZW5kY2hlY2tlciBlbmRjbGFzcyAnICtcbiAgICAgICdlbmRjbG9ja2luZyBlbmRjb25maWcgZW5kZnVuY3Rpb24gZW5kZ2VuZXJhdGUgZW5kZ3JvdXAgZW5kaW50ZXJmYWNlIGVuZG1vZHVsZSAnICtcbiAgICAgICdlbmRwYWNrYWdlIGVuZHByaW1pdGl2ZSBlbmRwcm9ncmFtIGVuZHByb3BlcnR5IGVuZHNwZWNpZnkgZW5kc2VxdWVuY2UgZW5kdGFibGUgJyArXG4gICAgICAnZW5kdGFzayBlbnVtIGV2ZW50IGV2ZW50dWFsbHkgZXhwZWN0IGV4cG9ydCBleHRlbmRzIGV4dGVybiBmaW5hbCBmaXJzdF9tYXRjaCBmb3IgJyArXG4gICAgICAnZm9yY2UgZm9yZWFjaCBmb3JldmVyIGZvcmsgZm9ya2pvaW4gZnVuY3Rpb24gZ2VuZXJhdGV8NSBnZW52YXIgZ2xvYmFsIGhpZ2h6MCBoaWdoejEgJyArXG4gICAgICAnaWYgaWZmIGlmbm9uZSBpZ25vcmVfYmlucyBpbGxlZ2FsX2JpbnMgaW1wbGVtZW50cyBpbXBsaWVzIGltcG9ydCBpbmNkaXIgaW5jbHVkZSAnICtcbiAgICAgICdpbml0aWFsIGlub3V0IGlucHV0IGluc2lkZSBpbnN0YW5jZSBpbnQgaW50ZWdlciBpbnRlcmNvbm5lY3QgaW50ZXJmYWNlIGludGVyc2VjdCAnICtcbiAgICAgICdqb2luIGpvaW5fYW55IGpvaW5fbm9uZSBsYXJnZSBsZXQgbGlibGlzdCBsaWJyYXJ5IGxvY2FsIGxvY2FscGFyYW0gbG9naWMgbG9uZ2ludCAnICtcbiAgICAgICdtYWNyb21vZHVsZSBtYXRjaGVzIG1lZGl1bSBtb2Rwb3J0IG1vZHVsZSBuYW5kIG5lZ2VkZ2UgbmV0dHlwZSBuZXcgbmV4dHRpbWUgbm1vcyAnICtcbiAgICAgICdub3Igbm9zaG93Y2FuY2VsbGVkIG5vdCBub3RpZjAgbm90aWYxIG9yIG91dHB1dCBwYWNrYWdlIHBhY2tlZCBwYXJhbWV0ZXIgcG1vcyAnICtcbiAgICAgICdwb3NlZGdlIHByaW1pdGl2ZSBwcmlvcml0eSBwcm9ncmFtIHByb3BlcnR5IHByb3RlY3RlZCBwdWxsMCBwdWxsMSBwdWxsZG93biBwdWxsdXAgJyArXG4gICAgICAncHVsc2VzdHlsZV9vbmRldGVjdCBwdWxzZXN0eWxlX29uZXZlbnQgcHVyZSByYW5kIHJhbmRjIHJhbmRjYXNlIHJhbmRzZXF1ZW5jZSByY21vcyAnICtcbiAgICAgICdyZWFsIHJlYWx0aW1lIHJlZiByZWcgcmVqZWN0X29uIHJlbGVhc2UgcmVwZWF0IHJlc3RyaWN0IHJldHVybiBybm1vcyBycG1vcyBydHJhbiAnICtcbiAgICAgICdydHJhbmlmMCBydHJhbmlmMSBzX2Fsd2F5cyBzX2V2ZW50dWFsbHkgc19uZXh0dGltZSBzX3VudGlsIHNfdW50aWxfd2l0aCBzY2FsYXJlZCAnICtcbiAgICAgICdzZXF1ZW5jZSBzaG9ydGludCBzaG9ydHJlYWwgc2hvd2NhbmNlbGxlZCBzaWduZWQgc21hbGwgc29mdCBzb2x2ZSBzcGVjaWZ5IHNwZWNwYXJhbSAnICtcbiAgICAgICdzdGF0aWMgc3RyaW5nIHN0cm9uZyBzdHJvbmcwIHN0cm9uZzEgc3RydWN0IHN1cGVyIHN1cHBseTAgc3VwcGx5MSBzeW5jX2FjY2VwdF9vbiAnICtcbiAgICAgICdzeW5jX3JlamVjdF9vbiB0YWJsZSB0YWdnZWQgdGFzayB0aGlzIHRocm91Z2hvdXQgdGltZSB0aW1lcHJlY2lzaW9uIHRpbWV1bml0IHRyYW4gJyArXG4gICAgICAndHJhbmlmMCB0cmFuaWYxIHRyaSB0cmkwIHRyaTEgdHJpYW5kIHRyaW9yIHRyaXJlZyB0eXBlIHR5cGVkZWYgdW5pb24gdW5pcXVlIHVuaXF1ZTAgJyArXG4gICAgICAndW5zaWduZWQgdW50aWwgdW50aWxfd2l0aCB1bnR5cGVkIHVzZSB1d2lyZSB2YXIgdmVjdG9yZWQgdmlydHVhbCB2b2lkIHdhaXQgd2FpdF9vcmRlciAnICtcbiAgICAgICd3YW5kIHdlYWsgd2VhazAgd2VhazEgd2hpbGUgd2lsZGNhcmQgd2lyZSB3aXRoIHdpdGhpbiB3b3IgeG5vciB4b3InLFxuICAgIGxpdGVyYWw6XG4gICAgICAnbnVsbCcsXG4gICAgYnVpbHRfaW46XG4gICAgICAnJGZpbmlzaCAkc3RvcCAkZXhpdCAkZmF0YWwgJGVycm9yICR3YXJuaW5nICRpbmZvICRyZWFsdGltZSAkdGltZSAkcHJpbnR0aW1lc2NhbGUgJyArXG4gICAgICAnJGJpdHN0b3JlYWwgJGJpdHN0b3Nob3J0cmVhbCAkaXRvciAkc2lnbmVkICRjYXN0ICRiaXRzICRzdGltZSAkdGltZWZvcm1hdCAnICtcbiAgICAgICckcmVhbHRvYml0cyAkc2hvcnRyZWFsdG9iaXRzICRydG9pICR1bnNpZ25lZCAkYXNzZXJ0b24gJGFzc2VydGtpbGwgJGFzc2VydHBhc3NvbiAnICtcbiAgICAgICckYXNzZXJ0ZmFpbG9uICRhc3NlcnRub252YWN1b3Vzb24gJGFzc2VydG9mZiAkYXNzZXJ0Y29udHJvbCAkYXNzZXJ0cGFzc29mZiAnICtcbiAgICAgICckYXNzZXJ0ZmFpbG9mZiAkYXNzZXJ0dmFjdW91c29mZiAkaXN1bmJvdW5kZWQgJHNhbXBsZWQgJGZlbGwgJGNoYW5nZWQgJHBhc3RfZ2NsayAnICtcbiAgICAgICckZmVsbF9nY2xrICRjaGFuZ2VkX2djbGsgJHJpc2luZ19nY2xrICRzdGVhZHlfZ2NsayAkY292ZXJhZ2VfY29udHJvbCAnICtcbiAgICAgICckY292ZXJhZ2VfZ2V0ICRjb3ZlcmFnZV9zYXZlICRzZXRfY292ZXJhZ2VfZGJfbmFtZSAkcm9zZSAkc3RhYmxlICRwYXN0ICcgK1xuICAgICAgJyRyb3NlX2djbGsgJHN0YWJsZV9nY2xrICRmdXR1cmVfZ2NsayAkZmFsbGluZ19nY2xrICRjaGFuZ2luZ19nY2xrICRkaXNwbGF5ICcgK1xuICAgICAgJyRjb3ZlcmFnZV9nZXRfbWF4ICRjb3ZlcmFnZV9tZXJnZSAkZ2V0X2NvdmVyYWdlICRsb2FkX2NvdmVyYWdlX2RiICR0eXBlbmFtZSAnICtcbiAgICAgICckdW5wYWNrZWRfZGltZW5zaW9ucyAkbGVmdCAkbG93ICRpbmNyZW1lbnQgJGNsb2cyICRsbiAkbG9nMTAgJGV4cCAkc3FydCAkcG93ICcgK1xuICAgICAgJyRmbG9vciAkY2VpbCAkc2luICRjb3MgJHRhbiAkY291bnRiaXRzICRvbmVob3QgJGlzdW5rbm93biAkZmF0YWwgJHdhcm5pbmcgJyArXG4gICAgICAnJGRpbWVuc2lvbnMgJHJpZ2h0ICRoaWdoICRzaXplICRhc2luICRhY29zICRhdGFuICRhdGFuMiAkaHlwb3QgJHNpbmggJGNvc2ggJyArXG4gICAgICAnJHRhbmggJGFzaW5oICRhY29zaCAkYXRhbmggJGNvdW50b25lcyAkb25laG90MCAkZXJyb3IgJGluZm8gJHJhbmRvbSAnICtcbiAgICAgICckZGlzdF9jaGlfc3F1YXJlICRkaXN0X2VybGFuZyAkZGlzdF9leHBvbmVudGlhbCAkZGlzdF9ub3JtYWwgJGRpc3RfcG9pc3NvbiAnICtcbiAgICAgICckZGlzdF90ICRkaXN0X3VuaWZvcm0gJHFfaW5pdGlhbGl6ZSAkcV9yZW1vdmUgJHFfZXhhbSAkYXN5bmMkYW5kJGFycmF5ICcgK1xuICAgICAgJyRhc3luYyRuYW5kJGFycmF5ICRhc3luYyRvciRhcnJheSAkYXN5bmMkbm9yJGFycmF5ICRzeW5jJGFuZCRhcnJheSAnICtcbiAgICAgICckc3luYyRuYW5kJGFycmF5ICRzeW5jJG9yJGFycmF5ICRzeW5jJG5vciRhcnJheSAkcV9hZGQgJHFfZnVsbCAkcHNwcmludGYgJyArXG4gICAgICAnJGFzeW5jJGFuZCRwbGFuZSAkYXN5bmMkbmFuZCRwbGFuZSAkYXN5bmMkb3IkcGxhbmUgJGFzeW5jJG5vciRwbGFuZSAnICtcbiAgICAgICckc3luYyRhbmQkcGxhbmUgJHN5bmMkbmFuZCRwbGFuZSAkc3luYyRvciRwbGFuZSAkc3luYyRub3IkcGxhbmUgJHN5c3RlbSAnICtcbiAgICAgICckZGlzcGxheSAkZGlzcGxheWIgJGRpc3BsYXloICRkaXNwbGF5byAkc3Ryb2JlICRzdHJvYmViICRzdHJvYmVoICRzdHJvYmVvICcgK1xuICAgICAgJyR3cml0ZSAkcmVhZG1lbWIgJHJlYWRtZW1oICR3cml0ZW1lbWggJHZhbHVlJHBsdXNhcmdzICcgK1xuICAgICAgJyRkdW1wdmFycyAkZHVtcG9uICRkdW1wbGltaXQgJGR1bXBwb3J0cyAkZHVtcHBvcnRzb24gJGR1bXBwb3J0c2xpbWl0ICcgK1xuICAgICAgJyR3cml0ZWIgJHdyaXRlaCAkd3JpdGVvICRtb25pdG9yICRtb25pdG9yYiAkbW9uaXRvcmggJG1vbml0b3JvICR3cml0ZW1lbWIgJyArXG4gICAgICAnJGR1bXBmaWxlICRkdW1wb2ZmICRkdW1wYWxsICRkdW1wZmx1c2ggJGR1bXBwb3J0c29mZiAkZHVtcHBvcnRzYWxsICcgK1xuICAgICAgJyRkdW1wcG9ydHNmbHVzaCAkZmNsb3NlICRmZGlzcGxheSAkZmRpc3BsYXliICRmZGlzcGxheWggJGZkaXNwbGF5byAnICtcbiAgICAgICckZnN0cm9iZSAkZnN0cm9iZWIgJGZzdHJvYmVoICRmc3Ryb2JlbyAkc3dyaXRlICRzd3JpdGViICRzd3JpdGVoICcgK1xuICAgICAgJyRzd3JpdGVvICRmc2NhbmYgJGZyZWFkICRmc2VlayAkZmZsdXNoICRmZW9mICRmb3BlbiAkZndyaXRlICRmd3JpdGViICcgK1xuICAgICAgJyRmd3JpdGVoICRmd3JpdGVvICRmbW9uaXRvciAkZm1vbml0b3JiICRmbW9uaXRvcmggJGZtb25pdG9ybyAkc2Zvcm1hdCAnICtcbiAgICAgICckc2Zvcm1hdGYgJGZnZXRjICR1bmdldGMgJGZnZXRzICRzc2NhbmYgJHJld2luZCAkZnRlbGwgJGZlcnJvcidcbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdWZXJpbG9nJyxcbiAgICBhbGlhc2VzOiBbXG4gICAgICAndicsXG4gICAgICAnc3YnLFxuICAgICAgJ3N2aCdcbiAgICBdLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IGZhbHNlLFxuICAgIGtleXdvcmRzOiBTVl9LRVlXT1JEUyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgICAgIGNvbnRhaW5zOiBbIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSBdLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXGIoKFxcXFxkK1xcJyhifGh8b3xkfEJ8SHxPfEQpKVswLTl4elhaYS1mQS1GX10rKSdcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXEIoKFxcJyhifGh8b3xkfEJ8SHxPfEQpKVswLTl4elhaYS1mQS1GX10rKSdcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXGIoWzAtOV9dKSsnLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAgLyogcGFyYW1ldGVycyB0byBpbnN0YW5jZXMgKi9cbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndmFyaWFibGUnLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnI1xcXFwoKD8hcGFyYW1ldGVyKS4rXFxcXCknXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ1xcXFwuXFxcXHcrJyxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiAnYCcsXG4gICAgICAgIGVuZDogJyQnLFxuICAgICAgICBrZXl3b3Jkczoge1xuICAgICAgICAgICdtZXRhLWtleXdvcmQnOlxuICAgICAgICAgICAgJ2RlZmluZSBfX0ZJTEVfXyAnICtcbiAgICAgICAgICAgICdfX0xJTkVfXyBiZWdpbl9rZXl3b3JkcyBjZWxsZGVmaW5lIGRlZmF1bHRfbmV0dHlwZSBkZWZpbmUgJyArXG4gICAgICAgICAgICAnZWxzZSBlbHNpZiBlbmRfa2V5d29yZHMgZW5kY2VsbGRlZmluZSBlbmRpZiBpZmRlZiBpZm5kZWYgJyArXG4gICAgICAgICAgICAnaW5jbHVkZSBsaW5lIG5vdW5jb25uZWN0ZWRfZHJpdmUgcHJhZ21hIHJlc2V0YWxsIHRpbWVzY2FsZSAnICtcbiAgICAgICAgICAgICd1bmNvbm5lY3RlZF9kcml2ZSB1bmRlZiB1bmRlZmluZWFsbCdcbiAgICAgICAgfSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHZlcmlsb2c7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=