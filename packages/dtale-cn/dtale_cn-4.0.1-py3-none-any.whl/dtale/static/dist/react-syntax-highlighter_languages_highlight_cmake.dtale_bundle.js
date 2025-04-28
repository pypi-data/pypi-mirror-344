(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_cmake"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/cmake.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/cmake.js ***!
  \************************************************************************************************/
/***/ ((module) => {

/*
Language: CMake
Description: CMake is an open-source cross-platform system for build automation.
Author: Igor Kalnitsky <igor@kalnitsky.org>
Website: https://cmake.org
*/

/** @type LanguageFn */
function cmake(hljs) {
  return {
    name: 'CMake',
    aliases: ['cmake.in'],
    case_insensitive: true,
    keywords: {
      keyword:
        // scripting commands
        'break cmake_host_system_information cmake_minimum_required cmake_parse_arguments ' +
        'cmake_policy configure_file continue elseif else endforeach endfunction endif endmacro ' +
        'endwhile execute_process file find_file find_library find_package find_path ' +
        'find_program foreach function get_cmake_property get_directory_property ' +
        'get_filename_component get_property if include include_guard list macro ' +
        'mark_as_advanced math message option return separate_arguments ' +
        'set_directory_properties set_property set site_name string unset variable_watch while ' +
        // project commands
        'add_compile_definitions add_compile_options add_custom_command add_custom_target ' +
        'add_definitions add_dependencies add_executable add_library add_link_options ' +
        'add_subdirectory add_test aux_source_directory build_command create_test_sourcelist ' +
        'define_property enable_language enable_testing export fltk_wrap_ui ' +
        'get_source_file_property get_target_property get_test_property include_directories ' +
        'include_external_msproject include_regular_expression install link_directories ' +
        'link_libraries load_cache project qt_wrap_cpp qt_wrap_ui remove_definitions ' +
        'set_source_files_properties set_target_properties set_tests_properties source_group ' +
        'target_compile_definitions target_compile_features target_compile_options ' +
        'target_include_directories target_link_directories target_link_libraries ' +
        'target_link_options target_sources try_compile try_run ' +
        // CTest commands
        'ctest_build ctest_configure ctest_coverage ctest_empty_binary_directory ctest_memcheck ' +
        'ctest_read_custom_files ctest_run_script ctest_sleep ctest_start ctest_submit ' +
        'ctest_test ctest_update ctest_upload ' +
        // deprecated commands
        'build_name exec_program export_library_dependencies install_files install_programs ' +
        'install_targets load_command make_directory output_required_files remove ' +
        'subdir_depends subdirs use_mangled_mesa utility_source variable_requires write_file ' +
        'qt5_use_modules qt5_use_package qt5_wrap_cpp ' +
        // core keywords
        'on off true false and or not command policy target test exists is_newer_than ' +
        'is_directory is_symlink is_absolute matches less greater equal less_equal ' +
        'greater_equal strless strgreater strequal strless_equal strgreater_equal version_less ' +
        'version_greater version_equal version_less_equal version_greater_equal in_list defined'
    },
    contains: [
      {
        className: 'variable',
        begin: /\$\{/,
        end: /\}/
      },
      hljs.HASH_COMMENT_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.NUMBER_MODE
    ]
  };
}

module.exports = cmake;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY21ha2UuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQSxvQkFBb0I7QUFDcEIsZ0JBQWdCO0FBQ2hCLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2NtYWtlLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogQ01ha2VcbkRlc2NyaXB0aW9uOiBDTWFrZSBpcyBhbiBvcGVuLXNvdXJjZSBjcm9zcy1wbGF0Zm9ybSBzeXN0ZW0gZm9yIGJ1aWxkIGF1dG9tYXRpb24uXG5BdXRob3I6IElnb3IgS2Fsbml0c2t5IDxpZ29yQGthbG5pdHNreS5vcmc+XG5XZWJzaXRlOiBodHRwczovL2NtYWtlLm9yZ1xuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGNtYWtlKGhsanMpIHtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnQ01ha2UnLFxuICAgIGFsaWFzZXM6IFsnY21ha2UuaW4nXSxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBrZXl3b3JkOlxuICAgICAgICAvLyBzY3JpcHRpbmcgY29tbWFuZHNcbiAgICAgICAgJ2JyZWFrIGNtYWtlX2hvc3Rfc3lzdGVtX2luZm9ybWF0aW9uIGNtYWtlX21pbmltdW1fcmVxdWlyZWQgY21ha2VfcGFyc2VfYXJndW1lbnRzICcgK1xuICAgICAgICAnY21ha2VfcG9saWN5IGNvbmZpZ3VyZV9maWxlIGNvbnRpbnVlIGVsc2VpZiBlbHNlIGVuZGZvcmVhY2ggZW5kZnVuY3Rpb24gZW5kaWYgZW5kbWFjcm8gJyArXG4gICAgICAgICdlbmR3aGlsZSBleGVjdXRlX3Byb2Nlc3MgZmlsZSBmaW5kX2ZpbGUgZmluZF9saWJyYXJ5IGZpbmRfcGFja2FnZSBmaW5kX3BhdGggJyArXG4gICAgICAgICdmaW5kX3Byb2dyYW0gZm9yZWFjaCBmdW5jdGlvbiBnZXRfY21ha2VfcHJvcGVydHkgZ2V0X2RpcmVjdG9yeV9wcm9wZXJ0eSAnICtcbiAgICAgICAgJ2dldF9maWxlbmFtZV9jb21wb25lbnQgZ2V0X3Byb3BlcnR5IGlmIGluY2x1ZGUgaW5jbHVkZV9ndWFyZCBsaXN0IG1hY3JvICcgK1xuICAgICAgICAnbWFya19hc19hZHZhbmNlZCBtYXRoIG1lc3NhZ2Ugb3B0aW9uIHJldHVybiBzZXBhcmF0ZV9hcmd1bWVudHMgJyArXG4gICAgICAgICdzZXRfZGlyZWN0b3J5X3Byb3BlcnRpZXMgc2V0X3Byb3BlcnR5IHNldCBzaXRlX25hbWUgc3RyaW5nIHVuc2V0IHZhcmlhYmxlX3dhdGNoIHdoaWxlICcgK1xuICAgICAgICAvLyBwcm9qZWN0IGNvbW1hbmRzXG4gICAgICAgICdhZGRfY29tcGlsZV9kZWZpbml0aW9ucyBhZGRfY29tcGlsZV9vcHRpb25zIGFkZF9jdXN0b21fY29tbWFuZCBhZGRfY3VzdG9tX3RhcmdldCAnICtcbiAgICAgICAgJ2FkZF9kZWZpbml0aW9ucyBhZGRfZGVwZW5kZW5jaWVzIGFkZF9leGVjdXRhYmxlIGFkZF9saWJyYXJ5IGFkZF9saW5rX29wdGlvbnMgJyArXG4gICAgICAgICdhZGRfc3ViZGlyZWN0b3J5IGFkZF90ZXN0IGF1eF9zb3VyY2VfZGlyZWN0b3J5IGJ1aWxkX2NvbW1hbmQgY3JlYXRlX3Rlc3Rfc291cmNlbGlzdCAnICtcbiAgICAgICAgJ2RlZmluZV9wcm9wZXJ0eSBlbmFibGVfbGFuZ3VhZ2UgZW5hYmxlX3Rlc3RpbmcgZXhwb3J0IGZsdGtfd3JhcF91aSAnICtcbiAgICAgICAgJ2dldF9zb3VyY2VfZmlsZV9wcm9wZXJ0eSBnZXRfdGFyZ2V0X3Byb3BlcnR5IGdldF90ZXN0X3Byb3BlcnR5IGluY2x1ZGVfZGlyZWN0b3JpZXMgJyArXG4gICAgICAgICdpbmNsdWRlX2V4dGVybmFsX21zcHJvamVjdCBpbmNsdWRlX3JlZ3VsYXJfZXhwcmVzc2lvbiBpbnN0YWxsIGxpbmtfZGlyZWN0b3JpZXMgJyArXG4gICAgICAgICdsaW5rX2xpYnJhcmllcyBsb2FkX2NhY2hlIHByb2plY3QgcXRfd3JhcF9jcHAgcXRfd3JhcF91aSByZW1vdmVfZGVmaW5pdGlvbnMgJyArXG4gICAgICAgICdzZXRfc291cmNlX2ZpbGVzX3Byb3BlcnRpZXMgc2V0X3RhcmdldF9wcm9wZXJ0aWVzIHNldF90ZXN0c19wcm9wZXJ0aWVzIHNvdXJjZV9ncm91cCAnICtcbiAgICAgICAgJ3RhcmdldF9jb21waWxlX2RlZmluaXRpb25zIHRhcmdldF9jb21waWxlX2ZlYXR1cmVzIHRhcmdldF9jb21waWxlX29wdGlvbnMgJyArXG4gICAgICAgICd0YXJnZXRfaW5jbHVkZV9kaXJlY3RvcmllcyB0YXJnZXRfbGlua19kaXJlY3RvcmllcyB0YXJnZXRfbGlua19saWJyYXJpZXMgJyArXG4gICAgICAgICd0YXJnZXRfbGlua19vcHRpb25zIHRhcmdldF9zb3VyY2VzIHRyeV9jb21waWxlIHRyeV9ydW4gJyArXG4gICAgICAgIC8vIENUZXN0IGNvbW1hbmRzXG4gICAgICAgICdjdGVzdF9idWlsZCBjdGVzdF9jb25maWd1cmUgY3Rlc3RfY292ZXJhZ2UgY3Rlc3RfZW1wdHlfYmluYXJ5X2RpcmVjdG9yeSBjdGVzdF9tZW1jaGVjayAnICtcbiAgICAgICAgJ2N0ZXN0X3JlYWRfY3VzdG9tX2ZpbGVzIGN0ZXN0X3J1bl9zY3JpcHQgY3Rlc3Rfc2xlZXAgY3Rlc3Rfc3RhcnQgY3Rlc3Rfc3VibWl0ICcgK1xuICAgICAgICAnY3Rlc3RfdGVzdCBjdGVzdF91cGRhdGUgY3Rlc3RfdXBsb2FkICcgK1xuICAgICAgICAvLyBkZXByZWNhdGVkIGNvbW1hbmRzXG4gICAgICAgICdidWlsZF9uYW1lIGV4ZWNfcHJvZ3JhbSBleHBvcnRfbGlicmFyeV9kZXBlbmRlbmNpZXMgaW5zdGFsbF9maWxlcyBpbnN0YWxsX3Byb2dyYW1zICcgK1xuICAgICAgICAnaW5zdGFsbF90YXJnZXRzIGxvYWRfY29tbWFuZCBtYWtlX2RpcmVjdG9yeSBvdXRwdXRfcmVxdWlyZWRfZmlsZXMgcmVtb3ZlICcgK1xuICAgICAgICAnc3ViZGlyX2RlcGVuZHMgc3ViZGlycyB1c2VfbWFuZ2xlZF9tZXNhIHV0aWxpdHlfc291cmNlIHZhcmlhYmxlX3JlcXVpcmVzIHdyaXRlX2ZpbGUgJyArXG4gICAgICAgICdxdDVfdXNlX21vZHVsZXMgcXQ1X3VzZV9wYWNrYWdlIHF0NV93cmFwX2NwcCAnICtcbiAgICAgICAgLy8gY29yZSBrZXl3b3Jkc1xuICAgICAgICAnb24gb2ZmIHRydWUgZmFsc2UgYW5kIG9yIG5vdCBjb21tYW5kIHBvbGljeSB0YXJnZXQgdGVzdCBleGlzdHMgaXNfbmV3ZXJfdGhhbiAnICtcbiAgICAgICAgJ2lzX2RpcmVjdG9yeSBpc19zeW1saW5rIGlzX2Fic29sdXRlIG1hdGNoZXMgbGVzcyBncmVhdGVyIGVxdWFsIGxlc3NfZXF1YWwgJyArXG4gICAgICAgICdncmVhdGVyX2VxdWFsIHN0cmxlc3Mgc3RyZ3JlYXRlciBzdHJlcXVhbCBzdHJsZXNzX2VxdWFsIHN0cmdyZWF0ZXJfZXF1YWwgdmVyc2lvbl9sZXNzICcgK1xuICAgICAgICAndmVyc2lvbl9ncmVhdGVyIHZlcnNpb25fZXF1YWwgdmVyc2lvbl9sZXNzX2VxdWFsIHZlcnNpb25fZ3JlYXRlcl9lcXVhbCBpbl9saXN0IGRlZmluZWQnXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd2YXJpYWJsZScsXG4gICAgICAgIGJlZ2luOiAvXFwkXFx7LyxcbiAgICAgICAgZW5kOiAvXFx9L1xuICAgICAgfSxcbiAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5OVU1CRVJfTU9ERVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBjbWFrZTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==