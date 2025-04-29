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
var Transmitter_exports = {};
__export(Transmitter_exports, {
  Transmitter: () => Transmitter
});
module.exports = __toCommonJS(Transmitter_exports);
var import_TransmitterWrapper = require("./TransmitterWrapper.cjs");
class Transmitter {
  static sendCommand(messageArray) {
    return import_TransmitterWrapper.TransmitterWrapper.sendCommand(messageArray);
  }
  static setConfigSource(configSource) {
    return import_TransmitterWrapper.TransmitterWrapper.setConfigSource(configSource);
  }
  static setJavonetWorkingDirectory(workingDirectory) {
    return import_TransmitterWrapper.TransmitterWrapper.setJavonetWorkingDirectory(workingDirectory);
  }
}
__publicField(Transmitter, "activate", function(licenseKey) {
  return import_TransmitterWrapper.TransmitterWrapper.activate(licenseKey);
});
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  Transmitter
});
