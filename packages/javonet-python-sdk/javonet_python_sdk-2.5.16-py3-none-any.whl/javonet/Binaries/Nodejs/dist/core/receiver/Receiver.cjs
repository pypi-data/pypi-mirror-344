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
var Receiver_exports = {};
__export(Receiver_exports, {
  Receiver: () => Receiver
});
module.exports = __toCommonJS(Receiver_exports);
const import_meta = {};
var import_Interpreter = require("../interpreter/Interpreter.cjs");
var import_CommandSerializer = require("../protocol/CommandSerializer.cjs");
var import_Runtime = require("../../utils/Runtime.cjs");
var import_InMemoryConnectionData = require("../../utils/connectionData/InMemoryConnectionData.cjs");
let _RuntimeLogger = null;
const requireDynamic = (0, import_Runtime.getRequire)(import_meta.url);
class Receiver {
  Receiver() {
    if (!_RuntimeLogger) {
      const { RuntimeLogger } = require("../../utils/RuntimeLogger.cjs");
      _RuntimeLogger = RuntimeLogger;
    }
    _RuntimeLogger?.printRuntimeInfo();
  }
  /**
   * @param {number[]} messageByteArray
   */
  static sendCommand(messageByteArray) {
    return new import_CommandSerializer.CommandSerializer().serialize(
      new import_Interpreter.Interpreter().process(messageByteArray),
      this.connectionData
    );
  }
  /**
   * @param {Int8Array} messageByteArray
   * @returns {Int8Array}
   */
  static heartBeat(messageByteArray) {
    let response = new Int8Array(2);
    response[0] = messageByteArray[11];
    response[1] = messageByteArray[12] - 2;
    return response;
  }
}
__publicField(Receiver, "connectionData", new import_InMemoryConnectionData.InMemoryConnectionData());
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  Receiver
});
