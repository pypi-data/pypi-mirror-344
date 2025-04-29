"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __typeError = (msg) => {
  throw TypeError(msg);
};
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
var __accessCheck = (obj, member, msg) => member.has(obj) || __typeError("Cannot " + msg);
var __privateGet = (obj, member, getter) => (__accessCheck(obj, member, "read from private field"), getter ? getter.call(obj) : member.get(obj));
var __privateAdd = (obj, member, value) => member.has(obj) ? __typeError("Cannot add the same private member more than once") : member instanceof WeakSet ? member.add(obj) : member.set(obj, value);
var __privateSet = (obj, member, value, setter) => (__accessCheck(obj, member, "write to private field"), setter ? setter.call(obj, value) : member.set(obj, value), value);
var RuntimeContext_exports = {};
__export(RuntimeContext_exports, {
  RuntimeContext: () => RuntimeContext
});
module.exports = __toCommonJS(RuntimeContext_exports);
var import_Command = require("../utils/Command.cjs");
var import_CommandType = require("../utils/CommandType.cjs");
var import_InvocationContext = require("./InvocationContext.cjs");
var import_ConnectionType = require("../utils/ConnectionType.cjs");
var import_ExceptionThrower = require("../utils/exception/ExceptionThrower.cjs");
var import_RuntimeName = require("../utils/RuntimeName.cjs");
var import_Interpreter = require("../core/interpreter/Interpreter.cjs");
var import_DelegatesCache = require("../core/delegatesCache/DelegatesCache.cjs");
var _currentCommand, _responseCommand, _interpreter, _buildCommand, _encapsulatePayloadItem;
const _RuntimeContext = class _RuntimeContext {
  constructor(runtimeName, connectionData) {
    __privateAdd(this, _currentCommand);
    __privateAdd(this, _responseCommand);
    __privateAdd(this, _interpreter);
    __privateAdd(this, _buildCommand, function(command) {
      for (let i = 0; i < command.payload.length; i++) {
        command.payload[i] = __privateGet(this, _encapsulatePayloadItem).call(this, command.payload[i]);
      }
      return command.prependArgToPayload(__privateGet(this, _currentCommand));
    });
    __privateAdd(this, _encapsulatePayloadItem, function(payloadItem) {
      if (payloadItem instanceof import_Command.Command) {
        for (let i = 0; i < payloadItem.payload.length; i++) {
          payloadItem.payload[i] = __privateGet(this, _encapsulatePayloadItem).call(this, payloadItem.payload[i]);
        }
        return payloadItem;
      } else if (payloadItem instanceof import_InvocationContext.InvocationContext) {
        return payloadItem.get_current_command();
      } else if (payloadItem instanceof Array) {
        const copiedArray = payloadItem.map((item) => __privateGet(this, _encapsulatePayloadItem).call(this, item));
        return new import_Command.Command(this.runtimeName, import_CommandType.CommandType.Array, copiedArray);
      } else if (typeof payloadItem === "function") {
        let newArray = new Array(payloadItem.length + 1);
        for (let i = 0; i < newArray.length; i++) {
          newArray[i] = "object";
        }
        const args = [import_DelegatesCache.delegatesCacheInstance.addDelegate(payloadItem), import_RuntimeName.RuntimeName.Nodejs].push(
          ...newArray
        );
        return new import_Command.Command(this.runtimeName, import_CommandType.CommandType.PassDelegate, args);
      } else {
        return new import_Command.Command(this.runtimeName, import_CommandType.CommandType.Value, [payloadItem]);
      }
    });
    this.runtimeName = runtimeName;
    this.connectionData = connectionData;
    __privateSet(this, _currentCommand, null);
    __privateSet(this, _responseCommand, null);
    __privateSet(this, _interpreter, new import_Interpreter.Interpreter());
  }
  static getInstance(runtimeName, connectionData) {
    switch (connectionData.connectionType) {
      case import_ConnectionType.ConnectionType.IN_MEMORY:
        if (runtimeName in _RuntimeContext.memoryRuntimeContexts) {
          let runtimeCtx = _RuntimeContext.memoryRuntimeContexts[runtimeName];
          runtimeCtx.currentCommand = null;
          return runtimeCtx;
        } else {
          let runtimeCtx = new _RuntimeContext(runtimeName, connectionData);
          _RuntimeContext.memoryRuntimeContexts[runtimeName] = runtimeCtx;
          return runtimeCtx;
        }
      case import_ConnectionType.ConnectionType.TCP: {
        let key1 = runtimeName + JSON.stringify(connectionData);
        if (key1 in _RuntimeContext.networkRuntimeContexts) {
          let runtimeCtx = _RuntimeContext.networkRuntimeContexts[key1];
          runtimeCtx.currentCommand = null;
          return runtimeCtx;
        } else {
          let runtimeCtx = new _RuntimeContext(runtimeName, connectionData);
          _RuntimeContext.networkRuntimeContexts[key1] = runtimeCtx;
          return runtimeCtx;
        }
      }
      case import_ConnectionType.ConnectionType.WEB_SOCKET: {
        let key2 = runtimeName + JSON.stringify(connectionData);
        if (key2 in _RuntimeContext.webSocketRuntimeContexts) {
          let runtimeCtx = _RuntimeContext.webSocketRuntimeContexts[key2];
          runtimeCtx.currentCommand = null;
          return runtimeCtx;
        } else {
          let runtimeCtx = new _RuntimeContext(runtimeName, connectionData);
          _RuntimeContext.webSocketRuntimeContexts[key2] = runtimeCtx;
          return runtimeCtx;
        }
      }
      default:
        throw new Error("Invalid connection type");
    }
  }
  /**
   * Executes the current command. The initial state of RuntimeContext is non-materialized,
   * wrapping either a single command or a chain of recursively nested commands.
   * Commands become nested through each invocation of methods on RuntimeContext.
   * Each invocation triggers the creation of a new RuntimeContext instance wrapping the current command with a new parent command.
   * The developer can decide at any moment of the materialization for the context, taking full control of the chunks of the expression being transferred and processed on the target runtime.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/foundations/execute-method)
   * @method
   */
  execute() {
    __privateSet(this, _responseCommand, __privateGet(this, _interpreter).execute(__privateGet(this, _currentCommand), this.connectionData));
    __privateSet(this, _currentCommand, null);
    if (__privateGet(this, _responseCommand) === void 0) {
      throw new Error("responseCommand is undefined in Runtime Context execute method");
    }
    if (__privateGet(this, _responseCommand).commandType === import_CommandType.CommandType.Exception) {
      throw import_ExceptionThrower.ExceptionThrower.throwException(__privateGet(this, _responseCommand));
    }
  }
  /**
   * Adds a reference to a library. Javonet allows you to reference and use modules or packages written in various languages.
   * This method allows you to use any library from all supported technologies. The necessary libraries need to be referenced.
   * The argument is a relative or full path to the library. If the library has dependencies on other libraries, the latter needs to be added first.
   * After referencing the library, any objects stored in this package can be used. Use static classes, create instances, call methods, use fields and properties, and much more.
   * @param {string} libraryPath - The relative or full path to the library.
   * @returns {RuntimeContext} RuntimeContext instance.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/getting-started/adding-references-to-libraries)
   * @method
   */
  loadLibrary(libraryPath) {
    let localCommand = new import_Command.Command(this.runtimeName, import_CommandType.CommandType.LoadLibrary, [libraryPath]);
    __privateSet(this, _currentCommand, __privateGet(this, _buildCommand).call(this, localCommand));
    this.execute();
    return this;
  }
  /**
   * Retrieves a reference to a specific type. The type can be a class, interface or enum. The type can be retrieved from any referenced library.
   * @param {string} typeName - The full name of the type.
   * @param {...any} args - The arguments to be passed, if needed
   * @returns {InvocationContext} InvocationContext instance, that wraps the command to get the type.
   * @method
   */
  getType(typeName, ...args) {
    let localCommand = new import_Command.Command(this.runtimeName, import_CommandType.CommandType.GetType, [typeName, ...args]);
    __privateSet(this, _currentCommand, null);
    if (this.connectionData.connectionType === import_ConnectionType.ConnectionType.WEB_SOCKET) {
      return new import_InvocationContext.InvocationWsContext(
        this.runtimeName,
        this.connectionData,
        __privateGet(this, _buildCommand).call(this, localCommand)
      );
    }
    return new import_InvocationContext.InvocationContext(this.runtimeName, this.connectionData, __privateGet(this, _buildCommand).call(this, localCommand));
  }
  /**
   * Casts the provided value to a specific type. This method is used when invoking methods that require specific types of arguments.
   * The arguments include the target type and the value to be cast. The target type must be retrieved from the called runtime using the getType method.
   * After casting the value, it can be used as an argument when invoking methods.
   * @param {...any} args - The target type and the value to be cast.
   * @returns {InvocationContext} InvocationContext instance that wraps the command to cast the value.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/casting/casting)
   * @method
   */
  cast(...args) {
    let localCommand = new import_Command.Command(this.runtimeName, import_CommandType.CommandType.Cast, args);
    __privateSet(this, _currentCommand, null);
    if (this.connectionData.connectionType === import_ConnectionType.ConnectionType.WEB_SOCKET) {
      return new import_InvocationContext.InvocationWsContext(
        this.runtimeName,
        this.connectionData,
        __privateGet(this, _buildCommand).call(this, localCommand)
      );
    }
    return new import_InvocationContext.InvocationContext(this.runtimeName, this.connectionData, __privateGet(this, _buildCommand).call(this, localCommand));
  }
  /**
   * Retrieves a specific item from an enum type. This method is used when working with enums from the called runtime.
   * The arguments include the enum type and the name of the item. The enum type must be retrieved from the called runtime using the getType method.
   * After retrieving the item, it can be used as an argument when invoking methods or for other operations.
   * @param {...any} args - The enum type and the name of the item.
   * @returns {InvocationContext} InvocationContext instance that wraps the command to get the enum item.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/enums/using-enum-type)
   * @method
   */
  getEnumItem(...args) {
    let localCommand = new import_Command.Command(this.runtimeName, import_CommandType.CommandType.GetEnumItem, args);
    __privateSet(this, _currentCommand, null);
    if (this.connectionData.connectionType === import_ConnectionType.ConnectionType.WEB_SOCKET) {
      return new import_InvocationContext.InvocationWsContext(
        this.runtimeName,
        this.connectionData,
        __privateGet(this, _buildCommand).call(this, localCommand)
      );
    }
    return new import_InvocationContext.InvocationContext(this.runtimeName, this.connectionData, __privateGet(this, _buildCommand).call(this, localCommand));
  }
  /**
   * Creates a reference type argument that can be passed to a method with a ref parameter modifier. This method is used when working with methods from the called runtime that require arguments to be passed by reference.
   * The arguments include the value and optionally the type of the reference. The type must be retrieved from the called runtime using the getType method.
   * After creating the reference, it can be used as an argument when invoking methods.
   * @param {...any} args - The value and optionally the type of the reference.
   * @returns {InvocationContext} InvocationContext instance that wraps the command to create a reference as ref.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/methods-arguments/passing-arguments-by-reference-with-ref-keyword)
   * @method
   */
  asRef(...args) {
    let localCommand = new import_Command.Command(this.runtimeName, import_CommandType.CommandType.AsRef, args);
    __privateSet(this, _currentCommand, null);
    if (this.connectionData.connectionType === import_ConnectionType.ConnectionType.WEB_SOCKET) {
      return new import_InvocationContext.InvocationWsContext(
        this.runtimeName,
        this.connectionData,
        __privateGet(this, _buildCommand).call(this, localCommand)
      );
    }
    return new import_InvocationContext.InvocationContext(this.runtimeName, this.connectionData, __privateGet(this, _buildCommand).call(this, localCommand));
  }
  /**
   * Creates a reference type argument that can be passed to a method with an out parameter modifier. This method is used when working with methods from the called runtime that require arguments to be passed by reference.
   * The arguments include the value and optionally the type of the reference. The type must be retrieved from the called runtime using the getType method.
   * After creating the reference, it can be used as an argument when invoking methods.
   * @param {...any} args - The value and optionally the type of the reference.
   * @returns {InvocationContext} InvocationContext instance that wraps the command to create a reference as out.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/methods-arguments/passing-arguments-by-reference-with-out-keyword |Passing Arguments by Reference with out Keyword Guide)
   * @method
   */
  asOut(...args) {
    let localCommand = new import_Command.Command(this.runtimeName, import_CommandType.CommandType.AsOut, args);
    __privateSet(this, _currentCommand, null);
    if (this.connectionData.connectionType === import_ConnectionType.ConnectionType.WEB_SOCKET) {
      return new import_InvocationContext.InvocationWsContext(
        this.runtimeName,
        this.connectionData,
        __privateGet(this, _buildCommand).call(this, localCommand)
      );
    }
    return new import_InvocationContext.InvocationContext(this.runtimeName, this.connectionData, __privateGet(this, _buildCommand).call(this, localCommand));
  }
  /**
   * Invokes a function from the called runtime. This method is used when working with functions from the called runtime.
   * The arguments include the function name and the arguments to be passed to the function.
   * After invoking the function, the result can be used for further operations.
   * @param {string} functionName - The name of the function to invoke.
   * @param {...any} args - The arguments to be passed to the function.
   * @returns {InvocationContext} InvocationContext instance that wraps the command to invoke the function.
   * @see [Invoking Functions Guide](https://www.javonet.com/guides/v2/csharp/functions/invoking-functions)
   * @method
   */
  invokeGlobalFunction(functionName, ...args) {
    let localCommand = new import_Command.Command(this.runtimeName, import_CommandType.CommandType.InvokeGlobalFunction, [
      functionName,
      ...args
    ]);
    __privateSet(this, _currentCommand, null);
    if (this.connectionData.connectionType === import_ConnectionType.ConnectionType.WEB_SOCKET) {
      return new import_InvocationContext.InvocationWsContext(
        this.runtimeName,
        this.connectionData,
        __privateGet(this, _buildCommand).call(this, localCommand)
      );
    }
    return new import_InvocationContext.InvocationContext(this.runtimeName, this.connectionData, __privateGet(this, _buildCommand).call(this, localCommand));
  }
  healthCheck() {
    let localCommand = new import_Command.Command(this.runtimeName, import_CommandType.CommandType.Value, ["health_check"]);
    __privateSet(this, _currentCommand, __privateGet(this, _buildCommand).call(this, localCommand));
    this.execute();
  }
};
_currentCommand = new WeakMap();
_responseCommand = new WeakMap();
_interpreter = new WeakMap();
_buildCommand = new WeakMap();
_encapsulatePayloadItem = new WeakMap();
__publicField(_RuntimeContext, "memoryRuntimeContexts", /* @__PURE__ */ new Map());
__publicField(_RuntimeContext, "networkRuntimeContexts", /* @__PURE__ */ new Map());
__publicField(_RuntimeContext, "webSocketRuntimeContexts", /* @__PURE__ */ new Map());
let RuntimeContext = _RuntimeContext;
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  RuntimeContext
});
