"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var __publicField = (obj, key, value) => __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);
var NamespaceCache_exports = {};
__export(NamespaceCache_exports, {
  NamespaceCache: () => NamespaceCache
});
module.exports = __toCommonJS(NamespaceCache_exports);
const _NamespaceCache = class _NamespaceCache {
  constructor() {
    __publicField(this, "namespaceCache", []);
    if (_NamespaceCache._instance === null) {
      _NamespaceCache._instance = this;
    }
    return _NamespaceCache._instance;
  }
  cacheNamespace(namespaceRegex) {
    this.namespaceCache.push(namespaceRegex);
  }
  isNamespaceCacheEmpty() {
    return this.namespaceCache.length === 0;
  }
  isTypeAllowed(typeToCheck) {
    for (let pattern of this.namespaceCache) {
      if (new RegExp(pattern).test(typeToCheck.constructor.name)) {
        return true;
      }
    }
    return false;
  }
  getCachedNamespaces() {
    return this.namespaceCache;
  }
  clearCache() {
    this.namespaceCache = [];
    return 0;
  }
};
__publicField(_NamespaceCache, "_instance", null);
let NamespaceCache = _NamespaceCache;
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  NamespaceCache
});
