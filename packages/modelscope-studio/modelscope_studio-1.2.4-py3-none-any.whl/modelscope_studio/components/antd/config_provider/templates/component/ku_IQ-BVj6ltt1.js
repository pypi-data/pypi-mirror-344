import { c as m } from "./Index-DLHiPW3-.js";
import { i as f } from "./config-provider-o6c_3Xme.js";
import { k as s, a as c, b as d, c as k } from "./kmr_IQ-BFOnJ1Vw.js";
function p(i, n) {
  for (var l = 0; l < n.length; l++) {
    const e = n[l];
    if (typeof e != "string" && !Array.isArray(e)) {
      for (const r in e)
        if (r !== "default" && !(r in i)) {
          const o = Object.getOwnPropertyDescriptor(e, r);
          o && Object.defineProperty(i, r, o.get ? o : {
            enumerable: !0,
            get: () => e[r]
          });
        }
    }
  }
  return Object.freeze(Object.defineProperty(i, Symbol.toStringTag, {
    value: "Module"
  }));
}
var t = {}, a = f.default;
Object.defineProperty(t, "__esModule", {
  value: !0
});
t.default = void 0;
var _ = a(s), b = a(c), v = a(d), g = a(k);
const T = {
  locale: "ku-iq",
  Pagination: _.default,
  DatePicker: v.default,
  TimePicker: g.default,
  Calendar: b.default,
  Table: {
    filterTitle: "Menuê peldanka",
    filterConfirm: "Temam",
    filterReset: "Jê bibe",
    selectAll: "Hemî hilbijêre",
    selectInvert: "Hilbijartinan veguhere"
  },
  Modal: {
    okText: "Temam",
    cancelText: "Betal ke",
    justOkText: "Temam"
  },
  Popconfirm: {
    okText: "Temam",
    cancelText: "Betal ke"
  },
  Transfer: {
    titles: ["", ""],
    searchPlaceholder: "Lêgerîn",
    itemUnit: "tişt",
    itemsUnit: "tişt"
  },
  Upload: {
    uploading: "Bardike...",
    removeFile: "Pelê rabike",
    uploadError: "Xeta barkirine",
    previewFile: "Pelê pêşbibîne",
    downloadFile: "Pelê dakêşin"
  },
  Empty: {
    description: "Agahî tune"
  }
};
t.default = T;
var u = t;
const I = /* @__PURE__ */ m(u), y = /* @__PURE__ */ p({
  __proto__: null,
  default: I
}, [u]);
export {
  y as k
};
