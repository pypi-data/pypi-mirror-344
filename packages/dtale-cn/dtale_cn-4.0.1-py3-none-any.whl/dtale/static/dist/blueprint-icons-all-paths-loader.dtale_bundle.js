"use strict";
(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["blueprint-icons-all-paths-loader"],{

/***/ "./node_modules/@blueprintjs/icons/lib/esm/paths-loaders/allPathsLoader.js":
/*!*********************************************************************************!*\
  !*** ./node_modules/@blueprintjs/icons/lib/esm/paths-loaders/allPathsLoader.js ***!
  \*********************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   allPathsLoader: () => (/* binding */ allPathsLoader)
/* harmony export */ });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/@blueprintjs/icons/node_modules/tslib/tslib.es6.mjs");
/*
 * Copyright 2023 Palantir Technologies, Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * A simple module loader which concatenates all icon paths into a single chunk.
 */
var allPathsLoader = function (name, size) { return (0,tslib__WEBPACK_IMPORTED_MODULE_0__.__awaiter)(void 0, void 0, void 0, function () {
    var getIconPaths;
    return (0,tslib__WEBPACK_IMPORTED_MODULE_0__.__generator)(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, Promise.all(/*! import() | blueprint-icons-all-paths */[__webpack_require__.e("blueprint-icons-20px-paths"), __webpack_require__.e("blueprint-icons-16px-paths"), __webpack_require__.e("blueprint-icons-all-paths")]).then(__webpack_require__.bind(__webpack_require__, /*! ../allPaths */ "./node_modules/@blueprintjs/icons/lib/esm/allPaths.js"))];
            case 1:
                getIconPaths = (_a.sent()).getIconPaths;
                return [2 /*return*/, getIconPaths(name, size)];
        }
    });
}); };
//# sourceMappingURL=allPathsLoader.js.map

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiYmx1ZXByaW50LWljb25zLWFsbC1wYXRocy1sb2FkZXIuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQytDO0FBQy9DO0FBQ0E7QUFDQTtBQUNPLDZDQUE2QyxPQUFPLGdEQUFTO0FBQ3BFO0FBQ0EsV0FBVyxrREFBVztBQUN0QjtBQUNBLHlDQUF5QyxzVkFFWDtBQUM5QjtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTCxDQUFDO0FBQ0QiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9AYmx1ZXByaW50anMvaWNvbnMvbGliL2VzbS9wYXRocy1sb2FkZXJzL2FsbFBhdGhzTG9hZGVyLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG4gKiBDb3B5cmlnaHQgMjAyMyBQYWxhbnRpciBUZWNobm9sb2dpZXMsIEluYy4gQWxsIHJpZ2h0cyByZXNlcnZlZC5cbiAqXG4gKiBMaWNlbnNlZCB1bmRlciB0aGUgQXBhY2hlIExpY2Vuc2UsIFZlcnNpb24gMi4wICh0aGUgXCJMaWNlbnNlXCIpO1xuICogeW91IG1heSBub3QgdXNlIHRoaXMgZmlsZSBleGNlcHQgaW4gY29tcGxpYW5jZSB3aXRoIHRoZSBMaWNlbnNlLlxuICogWW91IG1heSBvYnRhaW4gYSBjb3B5IG9mIHRoZSBMaWNlbnNlIGF0XG4gKlxuICogICAgIGh0dHA6Ly93d3cuYXBhY2hlLm9yZy9saWNlbnNlcy9MSUNFTlNFLTIuMFxuICpcbiAqIFVubGVzcyByZXF1aXJlZCBieSBhcHBsaWNhYmxlIGxhdyBvciBhZ3JlZWQgdG8gaW4gd3JpdGluZywgc29mdHdhcmVcbiAqIGRpc3RyaWJ1dGVkIHVuZGVyIHRoZSBMaWNlbnNlIGlzIGRpc3RyaWJ1dGVkIG9uIGFuIFwiQVMgSVNcIiBCQVNJUyxcbiAqIFdJVEhPVVQgV0FSUkFOVElFUyBPUiBDT05ESVRJT05TIE9GIEFOWSBLSU5ELCBlaXRoZXIgZXhwcmVzcyBvciBpbXBsaWVkLlxuICogU2VlIHRoZSBMaWNlbnNlIGZvciB0aGUgc3BlY2lmaWMgbGFuZ3VhZ2UgZ292ZXJuaW5nIHBlcm1pc3Npb25zIGFuZFxuICogbGltaXRhdGlvbnMgdW5kZXIgdGhlIExpY2Vuc2UuXG4gKi9cbmltcG9ydCB7IF9fYXdhaXRlciwgX19nZW5lcmF0b3IgfSBmcm9tIFwidHNsaWJcIjtcbi8qKlxuICogQSBzaW1wbGUgbW9kdWxlIGxvYWRlciB3aGljaCBjb25jYXRlbmF0ZXMgYWxsIGljb24gcGF0aHMgaW50byBhIHNpbmdsZSBjaHVuay5cbiAqL1xuZXhwb3J0IHZhciBhbGxQYXRoc0xvYWRlciA9IGZ1bmN0aW9uIChuYW1lLCBzaXplKSB7IHJldHVybiBfX2F3YWl0ZXIodm9pZCAwLCB2b2lkIDAsIHZvaWQgMCwgZnVuY3Rpb24gKCkge1xuICAgIHZhciBnZXRJY29uUGF0aHM7XG4gICAgcmV0dXJuIF9fZ2VuZXJhdG9yKHRoaXMsIGZ1bmN0aW9uIChfYSkge1xuICAgICAgICBzd2l0Y2ggKF9hLmxhYmVsKSB7XG4gICAgICAgICAgICBjYXNlIDA6IHJldHVybiBbNCAvKnlpZWxkKi8sIGltcG9ydChcbiAgICAgICAgICAgICAgICAvKiB3ZWJwYWNrQ2h1bmtOYW1lOiBcImJsdWVwcmludC1pY29ucy1hbGwtcGF0aHNcIiAqL1xuICAgICAgICAgICAgICAgIFwiLi4vYWxsUGF0aHNcIildO1xuICAgICAgICAgICAgY2FzZSAxOlxuICAgICAgICAgICAgICAgIGdldEljb25QYXRocyA9IChfYS5zZW50KCkpLmdldEljb25QYXRocztcbiAgICAgICAgICAgICAgICByZXR1cm4gWzIgLypyZXR1cm4qLywgZ2V0SWNvblBhdGhzKG5hbWUsIHNpemUpXTtcbiAgICAgICAgfVxuICAgIH0pO1xufSk7IH07XG4vLyMgc291cmNlTWFwcGluZ1VSTD1hbGxQYXRoc0xvYWRlci5qcy5tYXAiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=