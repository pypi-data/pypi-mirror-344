import { i as Qr, a as Xt, r as Jr, b as ei, w as ot, g as ti, c as ee, d as ni, e as ri, o as ii } from "./Index-C-Lk2Vrv.js";
const R = window.ms_globals.React, f = window.ms_globals.React, Ur = window.ms_globals.React.forwardRef, me = window.ms_globals.React.useRef, $e = window.ms_globals.React.useState, Ee = window.ms_globals.React.useEffect, Xr = window.ms_globals.React.version, Gr = window.ms_globals.React.isValidElement, qr = window.ms_globals.React.useLayoutEffect, Kr = window.ms_globals.React.useImperativeHandle, Yr = window.ms_globals.React.memo, Ut = window.ms_globals.React.useMemo, Zr = window.ms_globals.React.useCallback, hn = window.ms_globals.ReactDOM, dt = window.ms_globals.ReactDOM.createPortal, oi = window.ms_globals.internalContext.useContextPropsContext, si = window.ms_globals.internalContext.useSuggestionOpenContext, ai = window.ms_globals.antdIcons.FileTextFilled, li = window.ms_globals.antdIcons.CloseCircleFilled, ci = window.ms_globals.antdIcons.FileExcelFilled, ui = window.ms_globals.antdIcons.FileImageFilled, di = window.ms_globals.antdIcons.FileMarkdownFilled, fi = window.ms_globals.antdIcons.FilePdfFilled, hi = window.ms_globals.antdIcons.FilePptFilled, pi = window.ms_globals.antdIcons.FileWordFilled, mi = window.ms_globals.antdIcons.FileZipFilled, gi = window.ms_globals.antdIcons.PlusOutlined, vi = window.ms_globals.antdIcons.LeftOutlined, bi = window.ms_globals.antdIcons.RightOutlined, yi = window.ms_globals.antdIcons.CloseOutlined, wi = window.ms_globals.antdIcons.ClearOutlined, Si = window.ms_globals.antdIcons.ArrowUpOutlined, xi = window.ms_globals.antdIcons.AudioMutedOutlined, Ci = window.ms_globals.antdIcons.AudioOutlined, Ei = window.ms_globals.antdIcons.CloudUploadOutlined, _i = window.ms_globals.antdIcons.LinkOutlined, Ri = window.ms_globals.antd.ConfigProvider, nr = window.ms_globals.antd.Upload, ze = window.ms_globals.antd.theme, Ti = window.ms_globals.antd.Progress, Pi = window.ms_globals.antd.Image, Ie = window.ms_globals.antd.Button, rr = window.ms_globals.antd.Flex, Ot = window.ms_globals.antd.Typography, Mi = window.ms_globals.antd.Input, Li = window.ms_globals.antd.Tooltip, Oi = window.ms_globals.antd.Badge, Gt = window.ms_globals.antdCssinjs.unit, At = window.ms_globals.antdCssinjs.token2CSSVar, pn = window.ms_globals.antdCssinjs.useStyleRegister, Ai = window.ms_globals.antdCssinjs.useCSSVarRegister, $i = window.ms_globals.antdCssinjs.createTheme, Ii = window.ms_globals.antdCssinjs.useCacheToken;
var ki = /\s/;
function Di(r) {
  for (var e = r.length; e-- && ki.test(r.charAt(e)); )
    ;
  return e;
}
var Ni = /^\s+/;
function Fi(r) {
  return r && r.slice(0, Di(r) + 1).replace(Ni, "");
}
var mn = NaN, Wi = /^[-+]0x[0-9a-f]+$/i, ji = /^0b[01]+$/i, Bi = /^0o[0-7]+$/i, Hi = parseInt;
function gn(r) {
  if (typeof r == "number")
    return r;
  if (Qr(r))
    return mn;
  if (Xt(r)) {
    var e = typeof r.valueOf == "function" ? r.valueOf() : r;
    r = Xt(e) ? e + "" : e;
  }
  if (typeof r != "string")
    return r === 0 ? r : +r;
  r = Fi(r);
  var t = ji.test(r);
  return t || Bi.test(r) ? Hi(r.slice(2), t ? 2 : 8) : Wi.test(r) ? mn : +r;
}
function zi() {
}
var $t = function() {
  return Jr.Date.now();
}, Vi = "Expected a function", Ui = Math.max, Xi = Math.min;
function Gi(r, e, t) {
  var n, i, o, s, a, c, l = 0, u = !1, d = !1, h = !0;
  if (typeof r != "function")
    throw new TypeError(Vi);
  e = gn(e) || 0, Xt(t) && (u = !!t.leading, d = "maxWait" in t, o = d ? Ui(gn(t.maxWait) || 0, e) : o, h = "trailing" in t ? !!t.trailing : h);
  function p(w) {
    var T = n, C = i;
    return n = i = void 0, l = w, s = r.apply(C, T), s;
  }
  function b(w) {
    return l = w, a = setTimeout(m, e), u ? p(w) : s;
  }
  function v(w) {
    var T = w - c, C = w - l, P = e - T;
    return d ? Xi(P, o - C) : P;
  }
  function g(w) {
    var T = w - c, C = w - l;
    return c === void 0 || T >= e || T < 0 || d && C >= o;
  }
  function m() {
    var w = $t();
    if (g(w))
      return x(w);
    a = setTimeout(m, v(w));
  }
  function x(w) {
    return a = void 0, h && n ? p(w) : (n = i = void 0, s);
  }
  function E() {
    a !== void 0 && clearTimeout(a), l = 0, n = c = i = a = void 0;
  }
  function y() {
    return a === void 0 ? s : x($t());
  }
  function _() {
    var w = $t(), T = g(w);
    if (n = arguments, i = this, c = w, T) {
      if (a === void 0)
        return b(c);
      if (d)
        return clearTimeout(a), a = setTimeout(m, e), p(c);
    }
    return a === void 0 && (a = setTimeout(m, e)), s;
  }
  return _.cancel = E, _.flush = y, _;
}
function qi(r, e) {
  return ei(r, e);
}
var ir = {
  exports: {}
}, pt = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ki = f, Yi = Symbol.for("react.element"), Zi = Symbol.for("react.fragment"), Qi = Object.prototype.hasOwnProperty, Ji = Ki.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, eo = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function or(r, e, t) {
  var n, i = {}, o = null, s = null;
  t !== void 0 && (o = "" + t), e.key !== void 0 && (o = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (n in e) Qi.call(e, n) && !eo.hasOwnProperty(n) && (i[n] = e[n]);
  if (r && r.defaultProps) for (n in e = r.defaultProps, e) i[n] === void 0 && (i[n] = e[n]);
  return {
    $$typeof: Yi,
    type: r,
    key: o,
    ref: s,
    props: i,
    _owner: Ji.current
  };
}
pt.Fragment = Zi;
pt.jsx = or;
pt.jsxs = or;
ir.exports = pt;
var re = ir.exports;
const {
  SvelteComponent: to,
  assign: vn,
  binding_callbacks: bn,
  check_outros: no,
  children: sr,
  claim_element: ar,
  claim_space: ro,
  component_subscribe: yn,
  compute_slots: io,
  create_slot: oo,
  detach: Le,
  element: lr,
  empty: wn,
  exclude_internal_props: Sn,
  get_all_dirty_from_scope: so,
  get_slot_changes: ao,
  group_outros: lo,
  init: co,
  insert_hydration: st,
  safe_not_equal: uo,
  set_custom_element_data: cr,
  space: fo,
  transition_in: at,
  transition_out: qt,
  update_slot_base: ho
} = window.__gradio__svelte__internal, {
  beforeUpdate: po,
  getContext: mo,
  onDestroy: go,
  setContext: vo
} = window.__gradio__svelte__internal;
function xn(r) {
  let e, t;
  const n = (
    /*#slots*/
    r[7].default
  ), i = oo(
    n,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      e = lr("svelte-slot"), i && i.c(), this.h();
    },
    l(o) {
      e = ar(o, "SVELTE-SLOT", {
        class: !0
      });
      var s = sr(e);
      i && i.l(s), s.forEach(Le), this.h();
    },
    h() {
      cr(e, "class", "svelte-1rt0kpf");
    },
    m(o, s) {
      st(o, e, s), i && i.m(e, null), r[9](e), t = !0;
    },
    p(o, s) {
      i && i.p && (!t || s & /*$$scope*/
      64) && ho(
        i,
        n,
        o,
        /*$$scope*/
        o[6],
        t ? ao(
          n,
          /*$$scope*/
          o[6],
          s,
          null
        ) : so(
          /*$$scope*/
          o[6]
        ),
        null
      );
    },
    i(o) {
      t || (at(i, o), t = !0);
    },
    o(o) {
      qt(i, o), t = !1;
    },
    d(o) {
      o && Le(e), i && i.d(o), r[9](null);
    }
  };
}
function bo(r) {
  let e, t, n, i, o = (
    /*$$slots*/
    r[4].default && xn(r)
  );
  return {
    c() {
      e = lr("react-portal-target"), t = fo(), o && o.c(), n = wn(), this.h();
    },
    l(s) {
      e = ar(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), sr(e).forEach(Le), t = ro(s), o && o.l(s), n = wn(), this.h();
    },
    h() {
      cr(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      st(s, e, a), r[8](e), st(s, t, a), o && o.m(s, a), st(s, n, a), i = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? o ? (o.p(s, a), a & /*$$slots*/
      16 && at(o, 1)) : (o = xn(s), o.c(), at(o, 1), o.m(n.parentNode, n)) : o && (lo(), qt(o, 1, 1, () => {
        o = null;
      }), no());
    },
    i(s) {
      i || (at(o), i = !0);
    },
    o(s) {
      qt(o), i = !1;
    },
    d(s) {
      s && (Le(e), Le(t), Le(n)), r[8](null), o && o.d(s);
    }
  };
}
function Cn(r) {
  const {
    svelteInit: e,
    ...t
  } = r;
  return t;
}
function yo(r, e, t) {
  let n, i, {
    $$slots: o = {},
    $$scope: s
  } = e;
  const a = io(o);
  let {
    svelteInit: c
  } = e;
  const l = ot(Cn(e)), u = ot();
  yn(r, u, (y) => t(0, n = y));
  const d = ot();
  yn(r, d, (y) => t(1, i = y));
  const h = [], p = mo("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: v,
    subSlotIndex: g
  } = ti() || {}, m = c({
    parent: p,
    props: l,
    target: u,
    slot: d,
    slotKey: b,
    slotIndex: v,
    subSlotIndex: g,
    onDestroy(y) {
      h.push(y);
    }
  });
  vo("$$ms-gr-react-wrapper", m), po(() => {
    l.set(Cn(e));
  }), go(() => {
    h.forEach((y) => y());
  });
  function x(y) {
    bn[y ? "unshift" : "push"](() => {
      n = y, u.set(n);
    });
  }
  function E(y) {
    bn[y ? "unshift" : "push"](() => {
      i = y, d.set(i);
    });
  }
  return r.$$set = (y) => {
    t(17, e = vn(vn({}, e), Sn(y))), "svelteInit" in y && t(5, c = y.svelteInit), "$$scope" in y && t(6, s = y.$$scope);
  }, e = Sn(e), [n, i, u, d, a, c, s, o, x, E];
}
class wo extends to {
  constructor(e) {
    super(), co(this, e, yo, bo, uo, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: Za
} = window.__gradio__svelte__internal, En = window.ms_globals.rerender, It = window.ms_globals.tree;
function So(r, e = {}) {
  function t(n) {
    const i = ot(), o = new wo({
      ...n,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: i,
            reactComponent: r,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? It;
          return c.nodes = [...c.nodes, a], En({
            createPortal: dt,
            node: It
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((l) => l.svelteInstance !== i), En({
              createPortal: dt,
              node: It
            });
          }), a;
        },
        ...n.props
      }
    });
    return i.set(o), o;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const xo = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Co(r) {
  return r ? Object.keys(r).reduce((e, t) => {
    const n = r[t];
    return e[t] = Eo(t, n), e;
  }, {}) : {};
}
function Eo(r, e) {
  return typeof e == "number" && !xo.includes(r) ? e + "px" : e;
}
function Kt(r) {
  const e = [], t = r.cloneNode(!1);
  if (r._reactElement) {
    const i = f.Children.toArray(r._reactElement.props.children).map((o) => {
      if (f.isValidElement(o) && o.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Kt(o.props.el);
        return f.cloneElement(o, {
          ...o.props,
          el: a,
          children: [...f.Children.toArray(o.props.children), ...s]
        });
      }
      return null;
    });
    return i.originalChildren = r._reactElement.props.children, e.push(dt(f.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: i
    }), t)), {
      clonedElement: t,
      portals: e
    };
  }
  Object.keys(r.getEventListeners()).forEach((i) => {
    r.getEventListeners(i).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      t.addEventListener(a, s, c);
    });
  });
  const n = Array.from(r.childNodes);
  for (let i = 0; i < n.length; i++) {
    const o = n[i];
    if (o.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Kt(o);
      e.push(...a), t.appendChild(s);
    } else o.nodeType === 3 && t.appendChild(o.cloneNode());
  }
  return {
    clonedElement: t,
    portals: e
  };
}
function _o(r, e) {
  r && (typeof r == "function" ? r(e) : r.current = e);
}
const Ke = Ur(({
  slot: r,
  clone: e,
  className: t,
  style: n,
  observeAttributes: i
}, o) => {
  const s = me(), [a, c] = $e([]), {
    forceClone: l
  } = oi(), u = l ? !0 : e;
  return Ee(() => {
    var v;
    if (!s.current || !r)
      return;
    let d = r;
    function h() {
      let g = d;
      if (d.tagName.toLowerCase() === "svelte-slot" && d.children.length === 1 && d.children[0] && (g = d.children[0], g.tagName.toLowerCase() === "react-portal-target" && g.children[0] && (g = g.children[0])), _o(o, g), t && g.classList.add(...t.split(" ")), n) {
        const m = Co(n);
        Object.keys(m).forEach((x) => {
          g.style[x] = m[x];
        });
      }
    }
    let p = null, b = null;
    if (u && window.MutationObserver) {
      let g = function() {
        var y, _, w;
        (y = s.current) != null && y.contains(d) && ((_ = s.current) == null || _.removeChild(d));
        const {
          portals: x,
          clonedElement: E
        } = Kt(r);
        d = E, c(x), d.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          h();
        }, 50), (w = s.current) == null || w.appendChild(d);
      };
      g();
      const m = Gi(() => {
        g(), p == null || p.disconnect(), p == null || p.observe(r, {
          childList: !0,
          subtree: !0,
          attributes: i
        });
      }, 50);
      p = new window.MutationObserver(m), p.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      d.style.display = "contents", h(), (v = s.current) == null || v.appendChild(d);
    return () => {
      var g, m;
      d.style.display = "", (g = s.current) != null && g.contains(d) && ((m = s.current) == null || m.removeChild(d)), p == null || p.disconnect();
    };
  }, [r, u, t, n, o, i, l]), f.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Ro = "1.1.0", To = /* @__PURE__ */ f.createContext({}), Po = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, ur = (r) => {
  const e = f.useContext(To);
  return f.useMemo(() => ({
    ...Po,
    ...e[r]
  }), [e[r]]);
};
function ge() {
  return ge = Object.assign ? Object.assign.bind() : function(r) {
    for (var e = 1; e < arguments.length; e++) {
      var t = arguments[e];
      for (var n in t) ({}).hasOwnProperty.call(t, n) && (r[n] = t[n]);
    }
    return r;
  }, ge.apply(null, arguments);
}
function Ve() {
  const {
    getPrefixCls: r,
    direction: e,
    csp: t,
    iconPrefixCls: n,
    theme: i
  } = f.useContext(Ri.ConfigContext);
  return {
    theme: i,
    getPrefixCls: r,
    direction: e,
    csp: t,
    iconPrefixCls: n
  };
}
function Re(r) {
  var e = R.useRef();
  e.current = r;
  var t = R.useCallback(function() {
    for (var n, i = arguments.length, o = new Array(i), s = 0; s < i; s++)
      o[s] = arguments[s];
    return (n = e.current) === null || n === void 0 ? void 0 : n.call.apply(n, [e].concat(o));
  }, []);
  return t;
}
function Mo(r) {
  if (Array.isArray(r)) return r;
}
function Lo(r, e) {
  var t = r == null ? null : typeof Symbol < "u" && r[Symbol.iterator] || r["@@iterator"];
  if (t != null) {
    var n, i, o, s, a = [], c = !0, l = !1;
    try {
      if (o = (t = t.call(r)).next, e === 0) {
        if (Object(t) !== t) return;
        c = !1;
      } else for (; !(c = (n = o.call(t)).done) && (a.push(n.value), a.length !== e); c = !0) ;
    } catch (u) {
      l = !0, i = u;
    } finally {
      try {
        if (!c && t.return != null && (s = t.return(), Object(s) !== s)) return;
      } finally {
        if (l) throw i;
      }
    }
    return a;
  }
}
function _n(r, e) {
  (e == null || e > r.length) && (e = r.length);
  for (var t = 0, n = Array(e); t < e; t++) n[t] = r[t];
  return n;
}
function Oo(r, e) {
  if (r) {
    if (typeof r == "string") return _n(r, e);
    var t = {}.toString.call(r).slice(8, -1);
    return t === "Object" && r.constructor && (t = r.constructor.name), t === "Map" || t === "Set" ? Array.from(r) : t === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _n(r, e) : void 0;
  }
}
function Ao() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ue(r, e) {
  return Mo(r) || Lo(r, e) || Oo(r, e) || Ao();
}
function mt() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var Rn = mt() ? R.useLayoutEffect : R.useEffect, $o = function(e, t) {
  var n = R.useRef(!0);
  Rn(function() {
    return e(n.current);
  }, t), Rn(function() {
    return n.current = !1, function() {
      n.current = !0;
    };
  }, []);
}, Tn = function(e, t) {
  $o(function(n) {
    if (!n)
      return e();
  }, t);
};
function Ue(r) {
  var e = R.useRef(!1), t = R.useState(r), n = ue(t, 2), i = n[0], o = n[1];
  R.useEffect(function() {
    return e.current = !1, function() {
      e.current = !0;
    };
  }, []);
  function s(a, c) {
    c && e.current || o(a);
  }
  return [i, s];
}
function kt(r) {
  return r !== void 0;
}
function an(r, e) {
  var t = e || {}, n = t.defaultValue, i = t.value, o = t.onChange, s = t.postState, a = Ue(function() {
    return kt(i) ? i : kt(n) ? typeof n == "function" ? n() : n : typeof r == "function" ? r() : r;
  }), c = ue(a, 2), l = c[0], u = c[1], d = i !== void 0 ? i : l, h = s ? s(d) : d, p = Re(o), b = Ue([d]), v = ue(b, 2), g = v[0], m = v[1];
  Tn(function() {
    var E = g[0];
    l !== E && p(l, E);
  }, [g]), Tn(function() {
    kt(i) || u(i);
  }, [i]);
  var x = Re(function(E, y) {
    u(E, y), m([d], y);
  });
  return [h, x];
}
function oe(r) {
  "@babel/helpers - typeof";
  return oe = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, oe(r);
}
var dr = {
  exports: {}
}, V = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ln = Symbol.for("react.element"), cn = Symbol.for("react.portal"), gt = Symbol.for("react.fragment"), vt = Symbol.for("react.strict_mode"), bt = Symbol.for("react.profiler"), yt = Symbol.for("react.provider"), wt = Symbol.for("react.context"), Io = Symbol.for("react.server_context"), St = Symbol.for("react.forward_ref"), xt = Symbol.for("react.suspense"), Ct = Symbol.for("react.suspense_list"), Et = Symbol.for("react.memo"), _t = Symbol.for("react.lazy"), ko = Symbol.for("react.offscreen"), fr;
fr = Symbol.for("react.module.reference");
function ve(r) {
  if (typeof r == "object" && r !== null) {
    var e = r.$$typeof;
    switch (e) {
      case ln:
        switch (r = r.type, r) {
          case gt:
          case bt:
          case vt:
          case xt:
          case Ct:
            return r;
          default:
            switch (r = r && r.$$typeof, r) {
              case Io:
              case wt:
              case St:
              case _t:
              case Et:
              case yt:
                return r;
              default:
                return e;
            }
        }
      case cn:
        return e;
    }
  }
}
V.ContextConsumer = wt;
V.ContextProvider = yt;
V.Element = ln;
V.ForwardRef = St;
V.Fragment = gt;
V.Lazy = _t;
V.Memo = Et;
V.Portal = cn;
V.Profiler = bt;
V.StrictMode = vt;
V.Suspense = xt;
V.SuspenseList = Ct;
V.isAsyncMode = function() {
  return !1;
};
V.isConcurrentMode = function() {
  return !1;
};
V.isContextConsumer = function(r) {
  return ve(r) === wt;
};
V.isContextProvider = function(r) {
  return ve(r) === yt;
};
V.isElement = function(r) {
  return typeof r == "object" && r !== null && r.$$typeof === ln;
};
V.isForwardRef = function(r) {
  return ve(r) === St;
};
V.isFragment = function(r) {
  return ve(r) === gt;
};
V.isLazy = function(r) {
  return ve(r) === _t;
};
V.isMemo = function(r) {
  return ve(r) === Et;
};
V.isPortal = function(r) {
  return ve(r) === cn;
};
V.isProfiler = function(r) {
  return ve(r) === bt;
};
V.isStrictMode = function(r) {
  return ve(r) === vt;
};
V.isSuspense = function(r) {
  return ve(r) === xt;
};
V.isSuspenseList = function(r) {
  return ve(r) === Ct;
};
V.isValidElementType = function(r) {
  return typeof r == "string" || typeof r == "function" || r === gt || r === bt || r === vt || r === xt || r === Ct || r === ko || typeof r == "object" && r !== null && (r.$$typeof === _t || r.$$typeof === Et || r.$$typeof === yt || r.$$typeof === wt || r.$$typeof === St || r.$$typeof === fr || r.getModuleId !== void 0);
};
V.typeOf = ve;
dr.exports = V;
var Dt = dr.exports, Do = Symbol.for("react.element"), No = Symbol.for("react.transitional.element"), Fo = Symbol.for("react.fragment");
function Wo(r) {
  return (
    // Base object type
    r && oe(r) === "object" && // React Element type
    (r.$$typeof === Do || r.$$typeof === No) && // React Fragment type
    r.type === Fo
  );
}
var jo = Number(Xr.split(".")[0]), Bo = function(e, t) {
  typeof e == "function" ? e(t) : oe(e) === "object" && e && "current" in e && (e.current = t);
}, Ho = function(e) {
  var t, n;
  if (!e)
    return !1;
  if (hr(e) && jo >= 19)
    return !0;
  var i = Dt.isMemo(e) ? e.type.type : e.type;
  return !(typeof i == "function" && !((t = i.prototype) !== null && t !== void 0 && t.render) && i.$$typeof !== Dt.ForwardRef || typeof e == "function" && !((n = e.prototype) !== null && n !== void 0 && n.render) && e.$$typeof !== Dt.ForwardRef);
};
function hr(r) {
  return /* @__PURE__ */ Gr(r) && !Wo(r);
}
var zo = function(e) {
  if (e && hr(e)) {
    var t = e;
    return t.props.propertyIsEnumerable("ref") ? t.props.ref : t.ref;
  }
  return null;
};
function Vo(r, e) {
  for (var t = r, n = 0; n < e.length; n += 1) {
    if (t == null)
      return;
    t = t[e[n]];
  }
  return t;
}
function Uo(r, e) {
  if (oe(r) != "object" || !r) return r;
  var t = r[Symbol.toPrimitive];
  if (t !== void 0) {
    var n = t.call(r, e);
    if (oe(n) != "object") return n;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(r);
}
function pr(r) {
  var e = Uo(r, "string");
  return oe(e) == "symbol" ? e : e + "";
}
function k(r, e, t) {
  return (e = pr(e)) in r ? Object.defineProperty(r, e, {
    value: t,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : r[e] = t, r;
}
function Pn(r, e) {
  var t = Object.keys(r);
  if (Object.getOwnPropertySymbols) {
    var n = Object.getOwnPropertySymbols(r);
    e && (n = n.filter(function(i) {
      return Object.getOwnPropertyDescriptor(r, i).enumerable;
    })), t.push.apply(t, n);
  }
  return t;
}
function $(r) {
  for (var e = 1; e < arguments.length; e++) {
    var t = arguments[e] != null ? arguments[e] : {};
    e % 2 ? Pn(Object(t), !0).forEach(function(n) {
      k(r, n, t[n]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(r, Object.getOwnPropertyDescriptors(t)) : Pn(Object(t)).forEach(function(n) {
      Object.defineProperty(r, n, Object.getOwnPropertyDescriptor(t, n));
    });
  }
  return r;
}
const Xe = /* @__PURE__ */ f.createContext(null);
function Mn(r) {
  const {
    getDropContainer: e,
    className: t,
    prefixCls: n,
    children: i
  } = r, {
    disabled: o
  } = f.useContext(Xe), [s, a] = f.useState(), [c, l] = f.useState(null);
  if (f.useEffect(() => {
    const h = e == null ? void 0 : e();
    s !== h && a(h);
  }, [e]), f.useEffect(() => {
    if (s) {
      const h = () => {
        l(!0);
      }, p = (g) => {
        g.preventDefault();
      }, b = (g) => {
        g.relatedTarget || l(!1);
      }, v = (g) => {
        l(!1), g.preventDefault();
      };
      return document.addEventListener("dragenter", h), document.addEventListener("dragover", p), document.addEventListener("dragleave", b), document.addEventListener("drop", v), () => {
        document.removeEventListener("dragenter", h), document.removeEventListener("dragover", p), document.removeEventListener("dragleave", b), document.removeEventListener("drop", v);
      };
    }
  }, [!!s]), !(e && s && !o))
    return null;
  const d = `${n}-drop-area`;
  return /* @__PURE__ */ dt(/* @__PURE__ */ f.createElement("div", {
    className: ee(d, t, {
      [`${d}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: c ? "block" : "none"
    }
  }, i), s);
}
function Ln(r) {
  return r instanceof HTMLElement || r instanceof SVGElement;
}
function Xo(r) {
  return r && oe(r) === "object" && Ln(r.nativeElement) ? r.nativeElement : Ln(r) ? r : null;
}
function Go(r) {
  var e = Xo(r);
  if (e)
    return e;
  if (r instanceof f.Component) {
    var t;
    return (t = hn.findDOMNode) === null || t === void 0 ? void 0 : t.call(hn, r);
  }
  return null;
}
function qo(r, e) {
  if (r == null) return {};
  var t = {};
  for (var n in r) if ({}.hasOwnProperty.call(r, n)) {
    if (e.indexOf(n) !== -1) continue;
    t[n] = r[n];
  }
  return t;
}
function On(r, e) {
  if (r == null) return {};
  var t, n, i = qo(r, e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(r);
    for (n = 0; n < o.length; n++) t = o[n], e.indexOf(t) === -1 && {}.propertyIsEnumerable.call(r, t) && (i[t] = r[t]);
  }
  return i;
}
var Ko = /* @__PURE__ */ R.createContext({});
function De(r, e) {
  if (!(r instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function An(r, e) {
  for (var t = 0; t < e.length; t++) {
    var n = e[t];
    n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(r, pr(n.key), n);
  }
}
function Ne(r, e, t) {
  return e && An(r.prototype, e), t && An(r, t), Object.defineProperty(r, "prototype", {
    writable: !1
  }), r;
}
function Yt(r, e) {
  return Yt = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(t, n) {
    return t.__proto__ = n, t;
  }, Yt(r, e);
}
function Rt(r, e) {
  if (typeof e != "function" && e !== null) throw new TypeError("Super expression must either be null or a function");
  r.prototype = Object.create(e && e.prototype, {
    constructor: {
      value: r,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(r, "prototype", {
    writable: !1
  }), e && Yt(r, e);
}
function ft(r) {
  return ft = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, ft(r);
}
function mr() {
  try {
    var r = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (mr = function() {
    return !!r;
  })();
}
function Te(r) {
  if (r === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return r;
}
function Yo(r, e) {
  if (e && (oe(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return Te(r);
}
function Tt(r) {
  var e = mr();
  return function() {
    var t, n = ft(r);
    if (e) {
      var i = ft(this).constructor;
      t = Reflect.construct(n, arguments, i);
    } else t = n.apply(this, arguments);
    return Yo(this, t);
  };
}
var Zo = /* @__PURE__ */ function(r) {
  Rt(t, r);
  var e = Tt(t);
  function t() {
    return De(this, t), e.apply(this, arguments);
  }
  return Ne(t, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), t;
}(R.Component);
function Qo(r) {
  var e = R.useReducer(function(a) {
    return a + 1;
  }, 0), t = ue(e, 2), n = t[1], i = R.useRef(r), o = Re(function() {
    return i.current;
  }), s = Re(function(a) {
    i.current = typeof a == "function" ? a(i.current) : a, n();
  });
  return [o, s];
}
var _e = "none", Ye = "appear", Ze = "enter", Qe = "leave", $n = "none", ye = "prepare", Oe = "start", Ae = "active", un = "end", gr = "prepared";
function In(r, e) {
  var t = {};
  return t[r.toLowerCase()] = e.toLowerCase(), t["Webkit".concat(r)] = "webkit".concat(e), t["Moz".concat(r)] = "moz".concat(e), t["ms".concat(r)] = "MS".concat(e), t["O".concat(r)] = "o".concat(e.toLowerCase()), t;
}
function Jo(r, e) {
  var t = {
    animationend: In("Animation", "AnimationEnd"),
    transitionend: In("Transition", "TransitionEnd")
  };
  return r && ("AnimationEvent" in e || delete t.animationend.animation, "TransitionEvent" in e || delete t.transitionend.transition), t;
}
var es = Jo(mt(), typeof window < "u" ? window : {}), vr = {};
if (mt()) {
  var ts = document.createElement("div");
  vr = ts.style;
}
var Je = {};
function br(r) {
  if (Je[r])
    return Je[r];
  var e = es[r];
  if (e)
    for (var t = Object.keys(e), n = t.length, i = 0; i < n; i += 1) {
      var o = t[i];
      if (Object.prototype.hasOwnProperty.call(e, o) && o in vr)
        return Je[r] = e[o], Je[r];
    }
  return "";
}
var yr = br("animationend"), wr = br("transitionend"), Sr = !!(yr && wr), kn = yr || "animationend", Dn = wr || "transitionend";
function Nn(r, e) {
  if (!r) return null;
  if (oe(r) === "object") {
    var t = e.replace(/-\w/g, function(n) {
      return n[1].toUpperCase();
    });
    return r[t];
  }
  return "".concat(r, "-").concat(e);
}
const ns = function(r) {
  var e = me();
  function t(i) {
    i && (i.removeEventListener(Dn, r), i.removeEventListener(kn, r));
  }
  function n(i) {
    e.current && e.current !== i && t(e.current), i && i !== e.current && (i.addEventListener(Dn, r), i.addEventListener(kn, r), e.current = i);
  }
  return R.useEffect(function() {
    return function() {
      t(e.current);
    };
  }, []), [n, t];
};
var xr = mt() ? qr : Ee, Cr = function(e) {
  return +setTimeout(e, 16);
}, Er = function(e) {
  return clearTimeout(e);
};
typeof window < "u" && "requestAnimationFrame" in window && (Cr = function(e) {
  return window.requestAnimationFrame(e);
}, Er = function(e) {
  return window.cancelAnimationFrame(e);
});
var Fn = 0, dn = /* @__PURE__ */ new Map();
function _r(r) {
  dn.delete(r);
}
var Zt = function(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  Fn += 1;
  var n = Fn;
  function i(o) {
    if (o === 0)
      _r(n), e();
    else {
      var s = Cr(function() {
        i(o - 1);
      });
      dn.set(n, s);
    }
  }
  return i(t), n;
};
Zt.cancel = function(r) {
  var e = dn.get(r);
  return _r(r), Er(e);
};
const rs = function() {
  var r = R.useRef(null);
  function e() {
    Zt.cancel(r.current);
  }
  function t(n) {
    var i = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    e();
    var o = Zt(function() {
      i <= 1 ? n({
        isCanceled: function() {
          return o !== r.current;
        }
      }) : t(n, i - 1);
    });
    r.current = o;
  }
  return R.useEffect(function() {
    return function() {
      e();
    };
  }, []), [t, e];
};
var is = [ye, Oe, Ae, un], os = [ye, gr], Rr = !1, ss = !0;
function Tr(r) {
  return r === Ae || r === un;
}
const as = function(r, e, t) {
  var n = Ue($n), i = ue(n, 2), o = i[0], s = i[1], a = rs(), c = ue(a, 2), l = c[0], u = c[1];
  function d() {
    s(ye, !0);
  }
  var h = e ? os : is;
  return xr(function() {
    if (o !== $n && o !== un) {
      var p = h.indexOf(o), b = h[p + 1], v = t(o);
      v === Rr ? s(b, !0) : b && l(function(g) {
        function m() {
          g.isCanceled() || s(b, !0);
        }
        v === !0 ? m() : Promise.resolve(v).then(m);
      });
    }
  }, [r, o]), R.useEffect(function() {
    return function() {
      u();
    };
  }, []), [d, o];
};
function ls(r, e, t, n) {
  var i = n.motionEnter, o = i === void 0 ? !0 : i, s = n.motionAppear, a = s === void 0 ? !0 : s, c = n.motionLeave, l = c === void 0 ? !0 : c, u = n.motionDeadline, d = n.motionLeaveImmediately, h = n.onAppearPrepare, p = n.onEnterPrepare, b = n.onLeavePrepare, v = n.onAppearStart, g = n.onEnterStart, m = n.onLeaveStart, x = n.onAppearActive, E = n.onEnterActive, y = n.onLeaveActive, _ = n.onAppearEnd, w = n.onEnterEnd, T = n.onLeaveEnd, C = n.onVisibleChanged, P = Ue(), M = ue(P, 2), D = M[0], N = M[1], F = Qo(_e), W = ue(F, 2), L = W[0], H = W[1], O = Ue(null), z = ue(O, 2), S = z[0], se = z[1], te = L(), j = me(!1), Z = me(null);
  function X() {
    return t();
  }
  var Q = me(!1);
  function ae() {
    H(_e), se(null, !0);
  }
  var he = Re(function(I) {
    var Y = L();
    if (Y !== _e) {
      var ne = X();
      if (!(I && !I.deadline && I.target !== ne)) {
        var Pe = Q.current, Ce;
        Y === Ye && Pe ? Ce = _ == null ? void 0 : _(ne, I) : Y === Ze && Pe ? Ce = w == null ? void 0 : w(ne, I) : Y === Qe && Pe && (Ce = T == null ? void 0 : T(ne, I)), Pe && Ce !== !1 && ae();
      }
    }
  }), we = ns(he), xe = ue(we, 1), U = xe[0], A = function(Y) {
    switch (Y) {
      case Ye:
        return k(k(k({}, ye, h), Oe, v), Ae, x);
      case Ze:
        return k(k(k({}, ye, p), Oe, g), Ae, E);
      case Qe:
        return k(k(k({}, ye, b), Oe, m), Ae, y);
      default:
        return {};
    }
  }, B = R.useMemo(function() {
    return A(te);
  }, [te]), de = as(te, !r, function(I) {
    if (I === ye) {
      var Y = B[ye];
      return Y ? Y(X()) : Rr;
    }
    if (le in B) {
      var ne;
      se(((ne = B[le]) === null || ne === void 0 ? void 0 : ne.call(B, X(), null)) || null);
    }
    return le === Ae && te !== _e && (U(X()), u > 0 && (clearTimeout(Z.current), Z.current = setTimeout(function() {
      he({
        deadline: !0
      });
    }, u))), le === gr && ae(), ss;
  }), K = ue(de, 2), J = K[0], le = K[1], fe = Tr(le);
  Q.current = fe;
  var G = me(null);
  xr(function() {
    if (!(j.current && G.current === e)) {
      N(e);
      var I = j.current;
      j.current = !0;
      var Y;
      !I && e && a && (Y = Ye), I && e && o && (Y = Ze), (I && !e && l || !I && d && !e && l) && (Y = Qe);
      var ne = A(Y);
      Y && (r || ne[ye]) ? (H(Y), J()) : H(_e), G.current = e;
    }
  }, [e]), Ee(function() {
    // Cancel appear
    (te === Ye && !a || // Cancel enter
    te === Ze && !o || // Cancel leave
    te === Qe && !l) && H(_e);
  }, [a, o, l]), Ee(function() {
    return function() {
      j.current = !1, clearTimeout(Z.current);
    };
  }, []);
  var pe = R.useRef(!1);
  Ee(function() {
    D && (pe.current = !0), D !== void 0 && te === _e && ((pe.current || D) && (C == null || C(D)), pe.current = !0);
  }, [D, te]);
  var be = S;
  return B[ye] && le === Oe && (be = $({
    transition: "none"
  }, be)), [te, le, be, D ?? e];
}
function cs(r) {
  var e = r;
  oe(r) === "object" && (e = r.transitionSupport);
  function t(i, o) {
    return !!(i.motionName && e && o !== !1);
  }
  var n = /* @__PURE__ */ R.forwardRef(function(i, o) {
    var s = i.visible, a = s === void 0 ? !0 : s, c = i.removeOnLeave, l = c === void 0 ? !0 : c, u = i.forceRender, d = i.children, h = i.motionName, p = i.leavedClassName, b = i.eventProps, v = R.useContext(Ko), g = v.motion, m = t(i, g), x = me(), E = me();
    function y() {
      try {
        return x.current instanceof HTMLElement ? x.current : Go(E.current);
      } catch {
        return null;
      }
    }
    var _ = ls(m, a, y, i), w = ue(_, 4), T = w[0], C = w[1], P = w[2], M = w[3], D = R.useRef(M);
    M && (D.current = !0);
    var N = R.useCallback(function(z) {
      x.current = z, Bo(o, z);
    }, [o]), F, W = $($({}, b), {}, {
      visible: a
    });
    if (!d)
      F = null;
    else if (T === _e)
      M ? F = d($({}, W), N) : !l && D.current && p ? F = d($($({}, W), {}, {
        className: p
      }), N) : u || !l && !p ? F = d($($({}, W), {}, {
        style: {
          display: "none"
        }
      }), N) : F = null;
    else {
      var L;
      C === ye ? L = "prepare" : Tr(C) ? L = "active" : C === Oe && (L = "start");
      var H = Nn(h, "".concat(T, "-").concat(L));
      F = d($($({}, W), {}, {
        className: ee(Nn(h, T), k(k({}, H, H && L), h, typeof h == "string")),
        style: P
      }), N);
    }
    if (/* @__PURE__ */ R.isValidElement(F) && Ho(F)) {
      var O = zo(F);
      O || (F = /* @__PURE__ */ R.cloneElement(F, {
        ref: N
      }));
    }
    return /* @__PURE__ */ R.createElement(Zo, {
      ref: E
    }, F);
  });
  return n.displayName = "CSSMotion", n;
}
const Pr = cs(Sr);
var Qt = "add", Jt = "keep", en = "remove", Nt = "removed";
function us(r) {
  var e;
  return r && oe(r) === "object" && "key" in r ? e = r : e = {
    key: r
  }, $($({}, e), {}, {
    key: String(e.key)
  });
}
function tn() {
  var r = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return r.map(us);
}
function ds() {
  var r = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], t = [], n = 0, i = e.length, o = tn(r), s = tn(e);
  o.forEach(function(l) {
    for (var u = !1, d = n; d < i; d += 1) {
      var h = s[d];
      if (h.key === l.key) {
        n < d && (t = t.concat(s.slice(n, d).map(function(p) {
          return $($({}, p), {}, {
            status: Qt
          });
        })), n = d), t.push($($({}, h), {}, {
          status: Jt
        })), n += 1, u = !0;
        break;
      }
    }
    u || t.push($($({}, l), {}, {
      status: en
    }));
  }), n < i && (t = t.concat(s.slice(n).map(function(l) {
    return $($({}, l), {}, {
      status: Qt
    });
  })));
  var a = {};
  t.forEach(function(l) {
    var u = l.key;
    a[u] = (a[u] || 0) + 1;
  });
  var c = Object.keys(a).filter(function(l) {
    return a[l] > 1;
  });
  return c.forEach(function(l) {
    t = t.filter(function(u) {
      var d = u.key, h = u.status;
      return d !== l || h !== en;
    }), t.forEach(function(u) {
      u.key === l && (u.status = Jt);
    });
  }), t;
}
var fs = ["component", "children", "onVisibleChanged", "onAllRemoved"], hs = ["status"], ps = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function ms(r) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Pr, t = /* @__PURE__ */ function(n) {
    Rt(o, n);
    var i = Tt(o);
    function o() {
      var s;
      De(this, o);
      for (var a = arguments.length, c = new Array(a), l = 0; l < a; l++)
        c[l] = arguments[l];
      return s = i.call.apply(i, [this].concat(c)), k(Te(s), "state", {
        keyEntities: []
      }), k(Te(s), "removeKey", function(u) {
        s.setState(function(d) {
          var h = d.keyEntities.map(function(p) {
            return p.key !== u ? p : $($({}, p), {}, {
              status: Nt
            });
          });
          return {
            keyEntities: h
          };
        }, function() {
          var d = s.state.keyEntities, h = d.filter(function(p) {
            var b = p.status;
            return b !== Nt;
          }).length;
          h === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return Ne(o, [{
      key: "render",
      value: function() {
        var a = this, c = this.state.keyEntities, l = this.props, u = l.component, d = l.children, h = l.onVisibleChanged;
        l.onAllRemoved;
        var p = On(l, fs), b = u || R.Fragment, v = {};
        return ps.forEach(function(g) {
          v[g] = p[g], delete p[g];
        }), delete p.keys, /* @__PURE__ */ R.createElement(b, p, c.map(function(g, m) {
          var x = g.status, E = On(g, hs), y = x === Qt || x === Jt;
          return /* @__PURE__ */ R.createElement(e, ge({}, v, {
            key: E.key,
            visible: y,
            eventProps: E,
            onVisibleChanged: function(w) {
              h == null || h(w, {
                key: E.key
              }), w || a.removeKey(E.key);
            }
          }), function(_, w) {
            return d($($({}, _), {}, {
              index: m
            }), w);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, c) {
        var l = a.keys, u = c.keyEntities, d = tn(l), h = ds(u, d);
        return {
          keyEntities: h.filter(function(p) {
            var b = u.find(function(v) {
              var g = v.key;
              return p.key === g;
            });
            return !(b && b.status === Nt && p.status === en);
          })
        };
      }
    }]), o;
  }(R.Component);
  return k(t, "defaultProps", {
    component: "div"
  }), t;
}
const gs = ms(Sr);
function vs(r, e) {
  const {
    children: t,
    upload: n,
    rootClassName: i
  } = r, o = f.useRef(null);
  return f.useImperativeHandle(e, () => o.current), /* @__PURE__ */ f.createElement(nr, ge({}, n, {
    showUploadList: !1,
    rootClassName: i,
    ref: o
  }), t);
}
const Mr = /* @__PURE__ */ f.forwardRef(vs);
var Lr = /* @__PURE__ */ Ne(function r() {
  De(this, r);
}), Or = "CALC_UNIT", bs = new RegExp(Or, "g");
function Ft(r) {
  return typeof r == "number" ? "".concat(r).concat(Or) : r;
}
var ys = /* @__PURE__ */ function(r) {
  Rt(t, r);
  var e = Tt(t);
  function t(n, i) {
    var o;
    De(this, t), o = e.call(this), k(Te(o), "result", ""), k(Te(o), "unitlessCssVar", void 0), k(Te(o), "lowPriority", void 0);
    var s = oe(n);
    return o.unitlessCssVar = i, n instanceof t ? o.result = "(".concat(n.result, ")") : s === "number" ? o.result = Ft(n) : s === "string" && (o.result = n), o;
  }
  return Ne(t, [{
    key: "add",
    value: function(i) {
      return i instanceof t ? this.result = "".concat(this.result, " + ").concat(i.getResult()) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " + ").concat(Ft(i))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(i) {
      return i instanceof t ? this.result = "".concat(this.result, " - ").concat(i.getResult()) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " - ").concat(Ft(i))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(i) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), i instanceof t ? this.result = "".concat(this.result, " * ").concat(i.getResult(!0)) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " * ").concat(i)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(i) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), i instanceof t ? this.result = "".concat(this.result, " / ").concat(i.getResult(!0)) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " / ").concat(i)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(i) {
      return this.lowPriority || i ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(i) {
      var o = this, s = i || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(l) {
        return o.result.includes(l);
      }) && (c = !1), this.result = this.result.replace(bs, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), t;
}(Lr), ws = /* @__PURE__ */ function(r) {
  Rt(t, r);
  var e = Tt(t);
  function t(n) {
    var i;
    return De(this, t), i = e.call(this), k(Te(i), "result", 0), n instanceof t ? i.result = n.result : typeof n == "number" && (i.result = n), i;
  }
  return Ne(t, [{
    key: "add",
    value: function(i) {
      return i instanceof t ? this.result += i.result : typeof i == "number" && (this.result += i), this;
    }
  }, {
    key: "sub",
    value: function(i) {
      return i instanceof t ? this.result -= i.result : typeof i == "number" && (this.result -= i), this;
    }
  }, {
    key: "mul",
    value: function(i) {
      return i instanceof t ? this.result *= i.result : typeof i == "number" && (this.result *= i), this;
    }
  }, {
    key: "div",
    value: function(i) {
      return i instanceof t ? this.result /= i.result : typeof i == "number" && (this.result /= i), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), t;
}(Lr), Ss = function(e, t) {
  var n = e === "css" ? ys : ws;
  return function(i) {
    return new n(i, t);
  };
}, Wn = function(e, t) {
  return "".concat([t, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function jn(r, e, t, n) {
  var i = $({}, e[r]);
  if (n != null && n.deprecatedTokens) {
    var o = n.deprecatedTokens;
    o.forEach(function(a) {
      var c = ue(a, 2), l = c[0], u = c[1];
      if (i != null && i[l] || i != null && i[u]) {
        var d;
        (d = i[u]) !== null && d !== void 0 || (i[u] = i == null ? void 0 : i[l]);
      }
    });
  }
  var s = $($({}, t), i);
  return Object.keys(s).forEach(function(a) {
    s[a] === e[a] && delete s[a];
  }), s;
}
var Ar = typeof CSSINJS_STATISTIC < "u", nn = !0;
function Pt() {
  for (var r = arguments.length, e = new Array(r), t = 0; t < r; t++)
    e[t] = arguments[t];
  if (!Ar)
    return Object.assign.apply(Object, [{}].concat(e));
  nn = !1;
  var n = {};
  return e.forEach(function(i) {
    if (oe(i) === "object") {
      var o = Object.keys(i);
      o.forEach(function(s) {
        Object.defineProperty(n, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return i[s];
          }
        });
      });
    }
  }), nn = !0, n;
}
var Bn = {};
function xs() {
}
var Cs = function(e) {
  var t, n = e, i = xs;
  return Ar && typeof Proxy < "u" && (t = /* @__PURE__ */ new Set(), n = new Proxy(e, {
    get: function(s, a) {
      if (nn) {
        var c;
        (c = t) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), i = function(s, a) {
    var c;
    Bn[s] = {
      global: Array.from(t),
      component: $($({}, (c = Bn[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: n,
    keys: t,
    flush: i
  };
};
function Hn(r, e, t) {
  if (typeof t == "function") {
    var n;
    return t(Pt(e, (n = e[r]) !== null && n !== void 0 ? n : {}));
  }
  return t ?? {};
}
function Es(r) {
  return r === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var t = arguments.length, n = new Array(t), i = 0; i < t; i++)
        n[i] = arguments[i];
      return "max(".concat(n.map(function(o) {
        return Gt(o);
      }).join(","), ")");
    },
    min: function() {
      for (var t = arguments.length, n = new Array(t), i = 0; i < t; i++)
        n[i] = arguments[i];
      return "min(".concat(n.map(function(o) {
        return Gt(o);
      }).join(","), ")");
    }
  };
}
var _s = 1e3 * 60 * 10, Rs = /* @__PURE__ */ function() {
  function r() {
    De(this, r), k(this, "map", /* @__PURE__ */ new Map()), k(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), k(this, "nextID", 0), k(this, "lastAccessBeat", /* @__PURE__ */ new Map()), k(this, "accessBeat", 0);
  }
  return Ne(r, [{
    key: "set",
    value: function(t, n) {
      this.clear();
      var i = this.getCompositeKey(t);
      this.map.set(i, n), this.lastAccessBeat.set(i, Date.now());
    }
  }, {
    key: "get",
    value: function(t) {
      var n = this.getCompositeKey(t), i = this.map.get(n);
      return this.lastAccessBeat.set(n, Date.now()), this.accessBeat += 1, i;
    }
  }, {
    key: "getCompositeKey",
    value: function(t) {
      var n = this, i = t.map(function(o) {
        return o && oe(o) === "object" ? "obj_".concat(n.getObjectID(o)) : "".concat(oe(o), "_").concat(o);
      });
      return i.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(t) {
      if (this.objectIDMap.has(t))
        return this.objectIDMap.get(t);
      var n = this.nextID;
      return this.objectIDMap.set(t, n), this.nextID += 1, n;
    }
  }, {
    key: "clear",
    value: function() {
      var t = this;
      if (this.accessBeat > 1e4) {
        var n = Date.now();
        this.lastAccessBeat.forEach(function(i, o) {
          n - i > _s && (t.map.delete(o), t.lastAccessBeat.delete(o));
        }), this.accessBeat = 0;
      }
    }
  }]), r;
}(), zn = new Rs();
function Ts(r, e) {
  return f.useMemo(function() {
    var t = zn.get(e);
    if (t)
      return t;
    var n = r();
    return zn.set(e, n), n;
  }, e);
}
var Ps = function() {
  return {};
};
function Ms(r) {
  var e = r.useCSP, t = e === void 0 ? Ps : e, n = r.useToken, i = r.usePrefix, o = r.getResetStyles, s = r.getCommonStyle, a = r.getCompUnitless;
  function c(h, p, b, v) {
    var g = Array.isArray(h) ? h[0] : h;
    function m(C) {
      return "".concat(String(g)).concat(C.slice(0, 1).toUpperCase()).concat(C.slice(1));
    }
    var x = (v == null ? void 0 : v.unitless) || {}, E = typeof a == "function" ? a(h) : {}, y = $($({}, E), {}, k({}, m("zIndexPopup"), !0));
    Object.keys(x).forEach(function(C) {
      y[m(C)] = x[C];
    });
    var _ = $($({}, v), {}, {
      unitless: y,
      prefixToken: m
    }), w = u(h, p, b, _), T = l(g, b, _);
    return function(C) {
      var P = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, M = w(C, P), D = ue(M, 2), N = D[1], F = T(P), W = ue(F, 2), L = W[0], H = W[1];
      return [L, N, H];
    };
  }
  function l(h, p, b) {
    var v = b.unitless, g = b.injectStyle, m = g === void 0 ? !0 : g, x = b.prefixToken, E = b.ignore, y = function(T) {
      var C = T.rootCls, P = T.cssVar, M = P === void 0 ? {} : P, D = n(), N = D.realToken;
      return Ai({
        path: [h],
        prefix: M.prefix,
        key: M.key,
        unitless: v,
        ignore: E,
        token: N,
        scope: C
      }, function() {
        var F = Hn(h, N, p), W = jn(h, N, F, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(F).forEach(function(L) {
          W[x(L)] = W[L], delete W[L];
        }), W;
      }), null;
    }, _ = function(T) {
      var C = n(), P = C.cssVar;
      return [function(M) {
        return m && P ? /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement(y, {
          rootCls: T,
          cssVar: P,
          component: h
        }), M) : M;
      }, P == null ? void 0 : P.key];
    };
    return _;
  }
  function u(h, p, b) {
    var v = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = Array.isArray(h) ? h : [h, h], m = ue(g, 1), x = m[0], E = g.join("-"), y = r.layer || {
      name: "antd"
    };
    return function(_) {
      var w = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : _, T = n(), C = T.theme, P = T.realToken, M = T.hashId, D = T.token, N = T.cssVar, F = i(), W = F.rootPrefixCls, L = F.iconPrefixCls, H = t(), O = N ? "css" : "js", z = Ts(function() {
        var X = /* @__PURE__ */ new Set();
        return N && Object.keys(v.unitless || {}).forEach(function(Q) {
          X.add(At(Q, N.prefix)), X.add(At(Q, Wn(x, N.prefix)));
        }), Ss(O, X);
      }, [O, x, N == null ? void 0 : N.prefix]), S = Es(O), se = S.max, te = S.min, j = {
        theme: C,
        token: D,
        hashId: M,
        nonce: function() {
          return H.nonce;
        },
        clientOnly: v.clientOnly,
        layer: y,
        // antd is always at top of styles
        order: v.order || -999
      };
      typeof o == "function" && pn($($({}, j), {}, {
        clientOnly: !1,
        path: ["Shared", W]
      }), function() {
        return o(D, {
          prefix: {
            rootPrefixCls: W,
            iconPrefixCls: L
          },
          csp: H
        });
      });
      var Z = pn($($({}, j), {}, {
        path: [E, _, L]
      }), function() {
        if (v.injectStyle === !1)
          return [];
        var X = Cs(D), Q = X.token, ae = X.flush, he = Hn(x, P, b), we = ".".concat(_), xe = jn(x, P, he, {
          deprecatedTokens: v.deprecatedTokens
        });
        N && he && oe(he) === "object" && Object.keys(he).forEach(function(de) {
          he[de] = "var(".concat(At(de, Wn(x, N.prefix)), ")");
        });
        var U = Pt(Q, {
          componentCls: we,
          prefixCls: _,
          iconCls: ".".concat(L),
          antCls: ".".concat(W),
          calc: z,
          // @ts-ignore
          max: se,
          // @ts-ignore
          min: te
        }, N ? he : xe), A = p(U, {
          hashId: M,
          prefixCls: _,
          rootPrefixCls: W,
          iconPrefixCls: L
        });
        ae(x, xe);
        var B = typeof s == "function" ? s(U, _, w, v.resetFont) : null;
        return [v.resetStyle === !1 ? null : B, A];
      });
      return [Z, M];
    };
  }
  function d(h, p, b) {
    var v = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = u(h, p, b, $({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, v)), m = function(E) {
      var y = E.prefixCls, _ = E.rootCls, w = _ === void 0 ? y : _;
      return g(y, w), null;
    };
    return m;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: d,
    genComponentStyleHook: u
  };
}
const ie = Math.round;
function Wt(r, e) {
  const t = r.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], n = t.map((i) => parseFloat(i));
  for (let i = 0; i < 3; i += 1)
    n[i] = e(n[i] || 0, t[i] || "", i);
  return t[3] ? n[3] = t[3].includes("%") ? n[3] / 100 : n[3] : n[3] = 1, n;
}
const Vn = (r, e, t) => t === 0 ? r : r / 100;
function We(r, e) {
  const t = e || 255;
  return r > t ? t : r < 0 ? 0 : r;
}
class Se {
  constructor(e) {
    k(this, "isValid", !0), k(this, "r", 0), k(this, "g", 0), k(this, "b", 0), k(this, "a", 1), k(this, "_h", void 0), k(this, "_s", void 0), k(this, "_l", void 0), k(this, "_v", void 0), k(this, "_max", void 0), k(this, "_min", void 0), k(this, "_brightness", void 0);
    function t(n) {
      return n[0] in e && n[1] in e && n[2] in e;
    }
    if (e) if (typeof e == "string") {
      let i = function(o) {
        return n.startsWith(o);
      };
      const n = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(n) ? this.fromHexString(n) : i("rgb") ? this.fromRgbString(n) : i("hsl") ? this.fromHslString(n) : (i("hsv") || i("hsb")) && this.fromHsvString(n);
    } else if (e instanceof Se)
      this.r = e.r, this.g = e.g, this.b = e.b, this.a = e.a, this._h = e._h, this._s = e._s, this._l = e._l, this._v = e._v;
    else if (t("rgb"))
      this.r = We(e.r), this.g = We(e.g), this.b = We(e.b), this.a = typeof e.a == "number" ? We(e.a, 1) : 1;
    else if (t("hsl"))
      this.fromHsl(e);
    else if (t("hsv"))
      this.fromHsv(e);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(e));
  }
  // ======================= Setter =======================
  setR(e) {
    return this._sc("r", e);
  }
  setG(e) {
    return this._sc("g", e);
  }
  setB(e) {
    return this._sc("b", e);
  }
  setA(e) {
    return this._sc("a", e, 1);
  }
  setHue(e) {
    const t = this.toHsv();
    return t.h = e, this._c(t);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function e(o) {
      const s = o / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const t = e(this.r), n = e(this.g), i = e(this.b);
    return 0.2126 * t + 0.7152 * n + 0.0722 * i;
  }
  getHue() {
    if (typeof this._h > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._h = 0 : this._h = ie(60 * (this.r === this.getMax() ? (this.g - this.b) / e + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / e + 2 : (this.r - this.g) / e + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._s = 0 : this._s = e / this.getMax();
    }
    return this._s;
  }
  getLightness() {
    return typeof this._l > "u" && (this._l = (this.getMax() + this.getMin()) / 510), this._l;
  }
  getValue() {
    return typeof this._v > "u" && (this._v = this.getMax() / 255), this._v;
  }
  /**
   * Returns the perceived brightness of the color, from 0-255.
   * Note: this is not the b of HSB
   * @see http://www.w3.org/TR/AERT#color-contrast
   */
  getBrightness() {
    return typeof this._brightness > "u" && (this._brightness = (this.r * 299 + this.g * 587 + this.b * 114) / 1e3), this._brightness;
  }
  // ======================== Func ========================
  darken(e = 10) {
    const t = this.getHue(), n = this.getSaturation();
    let i = this.getLightness() - e / 100;
    return i < 0 && (i = 0), this._c({
      h: t,
      s: n,
      l: i,
      a: this.a
    });
  }
  lighten(e = 10) {
    const t = this.getHue(), n = this.getSaturation();
    let i = this.getLightness() + e / 100;
    return i > 1 && (i = 1), this._c({
      h: t,
      s: n,
      l: i,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(e, t = 50) {
    const n = this._c(e), i = t / 100, o = (a) => (n[a] - this[a]) * i + this[a], s = {
      r: ie(o("r")),
      g: ie(o("g")),
      b: ie(o("b")),
      a: ie(o("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(e = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, e);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(e = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, e);
  }
  onBackground(e) {
    const t = this._c(e), n = this.a + t.a * (1 - this.a), i = (o) => ie((this[o] * this.a + t[o] * t.a * (1 - this.a)) / n);
    return this._c({
      r: i("r"),
      g: i("g"),
      b: i("b"),
      a: n
    });
  }
  // ======================= Status =======================
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return this.getBrightness() >= 128;
  }
  // ======================== MISC ========================
  equals(e) {
    return this.r === e.r && this.g === e.g && this.b === e.b && this.a === e.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let e = "#";
    const t = (this.r || 0).toString(16);
    e += t.length === 2 ? t : "0" + t;
    const n = (this.g || 0).toString(16);
    e += n.length === 2 ? n : "0" + n;
    const i = (this.b || 0).toString(16);
    if (e += i.length === 2 ? i : "0" + i, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const o = ie(this.a * 255).toString(16);
      e += o.length === 2 ? o : "0" + o;
    }
    return e;
  }
  /** CSS support color pattern */
  toHsl() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      l: this.getLightness(),
      a: this.a
    };
  }
  /** CSS support color pattern */
  toHslString() {
    const e = this.getHue(), t = ie(this.getSaturation() * 100), n = ie(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${e},${t}%,${n}%,${this.a})` : `hsl(${e},${t}%,${n}%)`;
  }
  /** Same as toHsb */
  toHsv() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      v: this.getValue(),
      a: this.a
    };
  }
  toRgb() {
    return {
      r: this.r,
      g: this.g,
      b: this.b,
      a: this.a
    };
  }
  toRgbString() {
    return this.a !== 1 ? `rgba(${this.r},${this.g},${this.b},${this.a})` : `rgb(${this.r},${this.g},${this.b})`;
  }
  toString() {
    return this.toRgbString();
  }
  // ====================== Privates ======================
  /** Return a new FastColor object with one channel changed */
  _sc(e, t, n) {
    const i = this.clone();
    return i[e] = We(t, n), i;
  }
  _c(e) {
    return new this.constructor(e);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(e) {
    const t = e.replace("#", "");
    function n(i, o) {
      return parseInt(t[i] + t[o || i], 16);
    }
    t.length < 6 ? (this.r = n(0), this.g = n(1), this.b = n(2), this.a = t[3] ? n(3) / 255 : 1) : (this.r = n(0, 1), this.g = n(2, 3), this.b = n(4, 5), this.a = t[6] ? n(6, 7) / 255 : 1);
  }
  fromHsl({
    h: e,
    s: t,
    l: n,
    a: i
  }) {
    if (this._h = e % 360, this._s = t, this._l = n, this.a = typeof i == "number" ? i : 1, t <= 0) {
      const h = ie(n * 255);
      this.r = h, this.g = h, this.b = h;
    }
    let o = 0, s = 0, a = 0;
    const c = e / 60, l = (1 - Math.abs(2 * n - 1)) * t, u = l * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (o = l, s = u) : c >= 1 && c < 2 ? (o = u, s = l) : c >= 2 && c < 3 ? (s = l, a = u) : c >= 3 && c < 4 ? (s = u, a = l) : c >= 4 && c < 5 ? (o = u, a = l) : c >= 5 && c < 6 && (o = l, a = u);
    const d = n - l / 2;
    this.r = ie((o + d) * 255), this.g = ie((s + d) * 255), this.b = ie((a + d) * 255);
  }
  fromHsv({
    h: e,
    s: t,
    v: n,
    a: i
  }) {
    this._h = e % 360, this._s = t, this._v = n, this.a = typeof i == "number" ? i : 1;
    const o = ie(n * 255);
    if (this.r = o, this.g = o, this.b = o, t <= 0)
      return;
    const s = e / 60, a = Math.floor(s), c = s - a, l = ie(n * (1 - t) * 255), u = ie(n * (1 - t * c) * 255), d = ie(n * (1 - t * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = d, this.b = l;
        break;
      case 1:
        this.r = u, this.b = l;
        break;
      case 2:
        this.r = l, this.b = d;
        break;
      case 3:
        this.r = l, this.g = u;
        break;
      case 4:
        this.r = d, this.g = l;
        break;
      case 5:
      default:
        this.g = l, this.b = u;
        break;
    }
  }
  fromHsvString(e) {
    const t = Wt(e, Vn);
    this.fromHsv({
      h: t[0],
      s: t[1],
      v: t[2],
      a: t[3]
    });
  }
  fromHslString(e) {
    const t = Wt(e, Vn);
    this.fromHsl({
      h: t[0],
      s: t[1],
      l: t[2],
      a: t[3]
    });
  }
  fromRgbString(e) {
    const t = Wt(e, (n, i) => (
      // Convert percentage to number. e.g. 50% -> 128
      i.includes("%") ? ie(n / 100 * 255) : n
    ));
    this.r = t[0], this.g = t[1], this.b = t[2], this.a = t[3];
  }
}
const Ls = {
  blue: "#1677FF",
  purple: "#722ED1",
  cyan: "#13C2C2",
  green: "#52C41A",
  magenta: "#EB2F96",
  /**
   * @deprecated Use magenta instead
   */
  pink: "#EB2F96",
  red: "#F5222D",
  orange: "#FA8C16",
  yellow: "#FADB14",
  volcano: "#FA541C",
  geekblue: "#2F54EB",
  gold: "#FAAD14",
  lime: "#A0D911"
}, Os = Object.assign(Object.assign({}, Ls), {
  // Color
  colorPrimary: "#1677ff",
  colorSuccess: "#52c41a",
  colorWarning: "#faad14",
  colorError: "#ff4d4f",
  colorInfo: "#1677ff",
  colorLink: "",
  colorTextBase: "",
  colorBgBase: "",
  // Font
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
  fontFamilyCode: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace",
  fontSize: 14,
  // Line
  lineWidth: 1,
  lineType: "solid",
  // Motion
  motionUnit: 0.1,
  motionBase: 0,
  motionEaseOutCirc: "cubic-bezier(0.08, 0.82, 0.17, 1)",
  motionEaseInOutCirc: "cubic-bezier(0.78, 0.14, 0.15, 0.86)",
  motionEaseOut: "cubic-bezier(0.215, 0.61, 0.355, 1)",
  motionEaseInOut: "cubic-bezier(0.645, 0.045, 0.355, 1)",
  motionEaseOutBack: "cubic-bezier(0.12, 0.4, 0.29, 1.46)",
  motionEaseInBack: "cubic-bezier(0.71, -0.46, 0.88, 0.6)",
  motionEaseInQuint: "cubic-bezier(0.755, 0.05, 0.855, 0.06)",
  motionEaseOutQuint: "cubic-bezier(0.23, 1, 0.32, 1)",
  // Radius
  borderRadius: 6,
  // Size
  sizeUnit: 4,
  sizeStep: 4,
  sizePopupArrow: 16,
  // Control Base
  controlHeight: 32,
  // zIndex
  zIndexBase: 0,
  zIndexPopupBase: 1e3,
  // Image
  opacityImage: 1,
  // Wireframe
  wireframe: !1,
  // Motion
  motion: !0
});
function jt(r) {
  return r >= 0 && r <= 255;
}
function et(r, e) {
  const {
    r: t,
    g: n,
    b: i,
    a: o
  } = new Se(r).toRgb();
  if (o < 1)
    return r;
  const {
    r: s,
    g: a,
    b: c
  } = new Se(e).toRgb();
  for (let l = 0.01; l <= 1; l += 0.01) {
    const u = Math.round((t - s * (1 - l)) / l), d = Math.round((n - a * (1 - l)) / l), h = Math.round((i - c * (1 - l)) / l);
    if (jt(u) && jt(d) && jt(h))
      return new Se({
        r: u,
        g: d,
        b: h,
        a: Math.round(l * 100) / 100
      }).toRgbString();
  }
  return new Se({
    r: t,
    g: n,
    b: i,
    a: 1
  }).toRgbString();
}
var As = function(r, e) {
  var t = {};
  for (var n in r) Object.prototype.hasOwnProperty.call(r, n) && e.indexOf(n) < 0 && (t[n] = r[n]);
  if (r != null && typeof Object.getOwnPropertySymbols == "function") for (var i = 0, n = Object.getOwnPropertySymbols(r); i < n.length; i++)
    e.indexOf(n[i]) < 0 && Object.prototype.propertyIsEnumerable.call(r, n[i]) && (t[n[i]] = r[n[i]]);
  return t;
};
function $s(r) {
  const {
    override: e
  } = r, t = As(r, ["override"]), n = Object.assign({}, e);
  Object.keys(Os).forEach((h) => {
    delete n[h];
  });
  const i = Object.assign(Object.assign({}, t), n), o = 480, s = 576, a = 768, c = 992, l = 1200, u = 1600;
  if (i.motion === !1) {
    const h = "0s";
    i.motionDurationFast = h, i.motionDurationMid = h, i.motionDurationSlow = h;
  }
  return Object.assign(Object.assign(Object.assign({}, i), {
    // ============== Background ============== //
    colorFillContent: i.colorFillSecondary,
    colorFillContentHover: i.colorFill,
    colorFillAlter: i.colorFillQuaternary,
    colorBgContainerDisabled: i.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: i.colorBgContainer,
    colorSplit: et(i.colorBorderSecondary, i.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: i.colorTextQuaternary,
    colorTextDisabled: i.colorTextQuaternary,
    colorTextHeading: i.colorText,
    colorTextLabel: i.colorTextSecondary,
    colorTextDescription: i.colorTextTertiary,
    colorTextLightSolid: i.colorWhite,
    colorHighlight: i.colorError,
    colorBgTextHover: i.colorFillSecondary,
    colorBgTextActive: i.colorFill,
    colorIcon: i.colorTextTertiary,
    colorIconHover: i.colorText,
    colorErrorOutline: et(i.colorErrorBg, i.colorBgContainer),
    colorWarningOutline: et(i.colorWarningBg, i.colorBgContainer),
    // Font
    fontSizeIcon: i.fontSizeSM,
    // Line
    lineWidthFocus: i.lineWidth * 3,
    // Control
    lineWidth: i.lineWidth,
    controlOutlineWidth: i.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: i.controlHeight / 2,
    controlItemBgHover: i.colorFillTertiary,
    controlItemBgActive: i.colorPrimaryBg,
    controlItemBgActiveHover: i.colorPrimaryBgHover,
    controlItemBgActiveDisabled: i.colorFill,
    controlTmpOutline: i.colorFillQuaternary,
    controlOutline: et(i.colorPrimaryBg, i.colorBgContainer),
    lineType: i.lineType,
    borderRadius: i.borderRadius,
    borderRadiusXS: i.borderRadiusXS,
    borderRadiusSM: i.borderRadiusSM,
    borderRadiusLG: i.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: i.sizeXXS,
    paddingXS: i.sizeXS,
    paddingSM: i.sizeSM,
    padding: i.size,
    paddingMD: i.sizeMD,
    paddingLG: i.sizeLG,
    paddingXL: i.sizeXL,
    paddingContentHorizontalLG: i.sizeLG,
    paddingContentVerticalLG: i.sizeMS,
    paddingContentHorizontal: i.sizeMS,
    paddingContentVertical: i.sizeSM,
    paddingContentHorizontalSM: i.size,
    paddingContentVerticalSM: i.sizeXS,
    marginXXS: i.sizeXXS,
    marginXS: i.sizeXS,
    marginSM: i.sizeSM,
    margin: i.size,
    marginMD: i.sizeMD,
    marginLG: i.sizeLG,
    marginXL: i.sizeXL,
    marginXXL: i.sizeXXL,
    boxShadow: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
    screenXS: o,
    screenXSMin: o,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: c - 1,
    screenLG: c,
    screenLGMin: c,
    screenLGMax: l - 1,
    screenXL: l,
    screenXLMin: l,
    screenXLMax: u - 1,
    screenXXL: u,
    screenXXLMin: u,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new Se("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new Se("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new Se("rgba(0, 0, 0, 0.09)").toRgbString()}
    `,
    boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTabsOverflowLeft: "inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowRight: "inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowTop: "inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowBottom: "inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)"
  }), n);
}
const Is = {
  lineHeight: !0,
  lineHeightSM: !0,
  lineHeightLG: !0,
  lineHeightHeading1: !0,
  lineHeightHeading2: !0,
  lineHeightHeading3: !0,
  lineHeightHeading4: !0,
  lineHeightHeading5: !0,
  opacityLoading: !0,
  fontWeightStrong: !0,
  zIndexPopupBase: !0,
  zIndexBase: !0,
  opacityImage: !0
}, ks = {
  size: !0,
  sizeSM: !0,
  sizeLG: !0,
  sizeMD: !0,
  sizeXS: !0,
  sizeXXS: !0,
  sizeMS: !0,
  sizeXL: !0,
  sizeXXL: !0,
  sizeUnit: !0,
  sizeStep: !0,
  motionBase: !0,
  motionUnit: !0
}, Ds = $i(ze.defaultAlgorithm), Ns = {
  screenXS: !0,
  screenXSMin: !0,
  screenXSMax: !0,
  screenSM: !0,
  screenSMMin: !0,
  screenSMMax: !0,
  screenMD: !0,
  screenMDMin: !0,
  screenMDMax: !0,
  screenLG: !0,
  screenLGMin: !0,
  screenLGMax: !0,
  screenXL: !0,
  screenXLMin: !0,
  screenXLMax: !0,
  screenXXL: !0,
  screenXXLMin: !0
}, $r = (r, e, t) => {
  const n = t.getDerivativeToken(r), {
    override: i,
    ...o
  } = e;
  let s = {
    ...n,
    override: i
  };
  return s = $s(s), o && Object.entries(o).forEach(([a, c]) => {
    const {
      theme: l,
      ...u
    } = c;
    let d = u;
    l && (d = $r({
      ...s,
      ...u
    }, {
      override: u
    }, l)), s[a] = d;
  }), s;
};
function Fs() {
  const {
    token: r,
    hashed: e,
    theme: t = Ds,
    override: n,
    cssVar: i
  } = f.useContext(ze._internalContext), [o, s, a] = Ii(t, [ze.defaultSeed, r], {
    salt: `${Ro}-${e || ""}`,
    override: n,
    getComputedToken: $r,
    cssVar: i && {
      prefix: i.prefix,
      key: i.key,
      unitless: Is,
      ignore: ks,
      preserve: Ns
    }
  });
  return [t, a, e ? s : "", o, i];
}
const {
  genStyleHooks: Ir
} = Ms({
  usePrefix: () => {
    const {
      getPrefixCls: r,
      iconPrefixCls: e
    } = Ve();
    return {
      iconPrefixCls: e,
      rootPrefixCls: r()
    };
  },
  useToken: () => {
    const [r, e, t, n, i] = Fs();
    return {
      theme: r,
      realToken: e,
      hashId: t,
      token: n,
      cssVar: i
    };
  },
  useCSP: () => {
    const {
      csp: r
    } = Ve();
    return r ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), Ws = (r) => {
  const {
    componentCls: e,
    calc: t
  } = r, n = `${e}-list-card`, i = t(r.fontSize).mul(r.lineHeight).mul(2).add(r.paddingSM).add(r.paddingSM).equal();
  return {
    [n]: {
      borderRadius: r.borderRadius,
      position: "relative",
      background: r.colorFillContent,
      borderWidth: r.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${n}-name,${n}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${n}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${n}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: t(r.paddingSM).sub(r.lineWidth).equal(),
        paddingInlineStart: t(r.padding).add(r.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: r.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${n}-icon`]: {
          fontSize: t(r.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: t(r.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${n}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${n}-desc`]: {
          color: r.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: i,
        height: i,
        lineHeight: 1,
        [`&:not(${n}-status-error)`]: {
          border: 0
        },
        // Img
        img: {
          width: "100%",
          height: "100%",
          verticalAlign: "top",
          objectFit: "cover",
          borderRadius: "inherit"
        },
        // Mask
        [`${n}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${r.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${n}-status-error`]: {
          [`img, ${n}-img-mask`]: {
            borderRadius: t(r.borderRadius).sub(r.lineWidth).equal()
          },
          [`${n}-desc`]: {
            paddingInline: r.paddingXXS
          }
        },
        // Progress
        [`${n}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${n}-remove`]: {
        position: "absolute",
        top: 0,
        insetInlineEnd: 0,
        border: 0,
        padding: r.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: r.fontSize,
        cursor: "pointer",
        opacity: r.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: r.opacityLoading
        }
      },
      [`&:hover ${n}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: r.colorError,
        [`${n}-desc`]: {
          color: r.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((o) => `${o} ${r.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: t(r.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, rn = {
  "&, *": {
    boxSizing: "border-box"
  }
}, js = (r) => {
  const {
    componentCls: e,
    calc: t,
    antCls: n
  } = r, i = `${e}-drop-area`, o = `${e}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [i]: {
      position: "absolute",
      inset: 0,
      zIndex: r.zIndexPopupBase,
      ...rn,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${o}-inner`]: {
          display: "none"
        }
      },
      [o]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [o]: {
        height: "100%",
        borderRadius: r.borderRadius,
        borderWidth: r.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: r.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: r.colorBgPlaceholderHover,
        ...rn,
        [`${n}-upload-wrapper ${n}-upload${n}-upload-btn`]: {
          padding: 0
        },
        [`&${o}-drag-in`]: {
          borderColor: r.colorPrimaryHover
        },
        [`&${o}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${o}-inner`]: {
          gap: t(r.paddingXXS).div(2).equal()
        },
        [`${o}-icon`]: {
          fontSize: r.fontSizeHeading2,
          lineHeight: 1
        },
        [`${o}-title${o}-title`]: {
          margin: 0,
          fontSize: r.fontSize,
          lineHeight: r.lineHeight
        },
        [`${o}-description`]: {}
      }
    }
  };
}, Bs = (r) => {
  const {
    componentCls: e,
    calc: t
  } = r, n = `${e}-list`, i = t(r.fontSize).mul(r.lineHeight).mul(2).add(r.paddingSM).add(r.paddingSM).equal();
  return {
    [e]: {
      position: "relative",
      width: "100%",
      ...rn,
      // =============================== File List ===============================
      [n]: {
        display: "flex",
        flexWrap: "wrap",
        gap: r.paddingSM,
        fontSize: r.fontSize,
        lineHeight: r.lineHeight,
        color: r.colorText,
        paddingBlock: r.paddingSM,
        paddingInline: r.padding,
        width: "100%",
        background: r.colorBgContainer,
        // Hide scrollbar
        scrollbarWidth: "none",
        "-ms-overflow-style": "none",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        // Scroll
        "&-overflow-scrollX, &-overflow-scrollY": {
          "&:before, &:after": {
            content: '""',
            position: "absolute",
            opacity: 0,
            transition: `opacity ${r.motionDurationSlow}`,
            zIndex: 1
          }
        },
        "&-overflow-ping-start:before": {
          opacity: 1
        },
        "&-overflow-ping-end:after": {
          opacity: 1
        },
        "&-overflow-scrollX": {
          overflowX: "auto",
          overflowY: "hidden",
          flexWrap: "nowrap",
          "&:before, &:after": {
            insetBlock: 0,
            width: 8
          },
          "&:before": {
            insetInlineStart: 0,
            background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetInlineEnd: 0,
            background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:dir(rtl)": {
            "&:before": {
              background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            },
            "&:after": {
              background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            }
          }
        },
        "&-overflow-scrollY": {
          overflowX: "hidden",
          overflowY: "auto",
          maxHeight: t(i).mul(3).equal(),
          "&:before, &:after": {
            insetInline: 0,
            height: 8
          },
          "&:before": {
            insetBlockStart: 0,
            background: "linear-gradient(to bottom, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetBlockEnd: 0,
            background: "linear-gradient(to top, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          }
        },
        // ======================================================================
        // ==                              Upload                              ==
        // ======================================================================
        "&-upload-btn": {
          width: i,
          height: i,
          fontSize: r.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: r.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: r.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: r.padding
          }
        },
        "&:dir(ltr)": {
          [`&${n}-overflow-ping-start ${n}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${n}-overflow-ping-end ${n}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${n}-overflow-ping-end ${n}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${n}-overflow-ping-start ${n}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, Hs = (r) => {
  const {
    colorBgContainer: e
  } = r;
  return {
    colorBgPlaceholderHover: new Se(e).setA(0.85).toRgbString()
  };
}, kr = Ir("Attachments", (r) => {
  const e = Pt(r, {});
  return [js(e), Bs(e), Ws(e)];
}, Hs), zs = (r) => r.indexOf("image/") === 0, tt = 200;
function Vs(r) {
  return new Promise((e) => {
    if (!r || !r.type || !zs(r.type)) {
      e("");
      return;
    }
    const t = new Image();
    if (t.onload = () => {
      const {
        width: n,
        height: i
      } = t, o = n / i, s = o > 1 ? tt : tt * o, a = o > 1 ? tt / o : tt, c = document.createElement("canvas");
      c.width = s, c.height = a, c.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(c), c.getContext("2d").drawImage(t, 0, 0, s, a);
      const u = c.toDataURL();
      document.body.removeChild(c), window.URL.revokeObjectURL(t.src), e(u);
    }, t.crossOrigin = "anonymous", r.type.startsWith("image/svg+xml")) {
      const n = new FileReader();
      n.onload = () => {
        n.result && typeof n.result == "string" && (t.src = n.result);
      }, n.readAsDataURL(r);
    } else if (r.type.startsWith("image/gif")) {
      const n = new FileReader();
      n.onload = () => {
        n.result && e(n.result);
      }, n.readAsDataURL(r);
    } else
      t.src = window.URL.createObjectURL(r);
  });
}
function Us() {
  return /* @__PURE__ */ f.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    //xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ f.createElement("title", null, "audio"), /* @__PURE__ */ f.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ f.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function Xs(r) {
  const {
    percent: e
  } = r, {
    token: t
  } = ze.useToken();
  return /* @__PURE__ */ f.createElement(Ti, {
    type: "circle",
    percent: e,
    size: t.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (n) => /* @__PURE__ */ f.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (n || 0).toFixed(0), "%")
  });
}
function Gs() {
  return /* @__PURE__ */ f.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    // xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ f.createElement("title", null, "video"), /* @__PURE__ */ f.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ f.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const Bt = " ", on = "#8c8c8c", Dr = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], qs = [{
  icon: /* @__PURE__ */ f.createElement(ci, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ f.createElement(ui, null),
  color: on,
  ext: Dr
}, {
  icon: /* @__PURE__ */ f.createElement(di, null),
  color: on,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ f.createElement(fi, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ f.createElement(hi, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ f.createElement(pi, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ f.createElement(mi, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ f.createElement(Gs, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ f.createElement(Us, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function Un(r, e) {
  return e.some((t) => r.toLowerCase() === `.${t}`);
}
function Ks(r) {
  let e = r;
  const t = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let n = 0;
  for (; e >= 1024 && n < t.length - 1; )
    e /= 1024, n++;
  return `${e.toFixed(0)} ${t[n]}`;
}
function Ys(r, e) {
  const {
    prefixCls: t,
    item: n,
    onRemove: i,
    className: o,
    style: s,
    imageProps: a
  } = r, c = f.useContext(Xe), {
    disabled: l
  } = c || {}, {
    name: u,
    size: d,
    percent: h,
    status: p = "done",
    description: b
  } = n, {
    getPrefixCls: v
  } = Ve(), g = v("attachment", t), m = `${g}-list-card`, [x, E, y] = kr(g), [_, w] = f.useMemo(() => {
    const H = u || "", O = H.match(/^(.*)\.[^.]+$/);
    return O ? [O[1], H.slice(O[1].length)] : [H, ""];
  }, [u]), T = f.useMemo(() => Un(w, Dr), [w]), C = f.useMemo(() => b || (p === "uploading" ? `${h || 0}%` : p === "error" ? n.response || Bt : d ? Ks(d) : Bt), [p, h]), [P, M] = f.useMemo(() => {
    for (const {
      ext: H,
      icon: O,
      color: z
    } of qs)
      if (Un(w, H))
        return [O, z];
    return [/* @__PURE__ */ f.createElement(ai, {
      key: "defaultIcon"
    }), on];
  }, [w]), [D, N] = f.useState();
  f.useEffect(() => {
    if (n.originFileObj) {
      let H = !0;
      return Vs(n.originFileObj).then((O) => {
        H && N(O);
      }), () => {
        H = !1;
      };
    }
    N(void 0);
  }, [n.originFileObj]);
  let F = null;
  const W = n.thumbUrl || n.url || D, L = T && (n.originFileObj || W);
  return L ? F = /* @__PURE__ */ f.createElement(f.Fragment, null, W && /* @__PURE__ */ f.createElement(Pi, ge({}, a, {
    alt: "preview",
    src: W
  })), p !== "done" && /* @__PURE__ */ f.createElement("div", {
    className: `${m}-img-mask`
  }, p === "uploading" && h !== void 0 && /* @__PURE__ */ f.createElement(Xs, {
    percent: h,
    prefixCls: m
  }), p === "error" && /* @__PURE__ */ f.createElement("div", {
    className: `${m}-desc`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, C)))) : F = /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-icon`,
    style: {
      color: M
    }
  }, P), /* @__PURE__ */ f.createElement("div", {
    className: `${m}-content`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-name`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, _ ?? Bt), /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-suffix`
  }, w)), /* @__PURE__ */ f.createElement("div", {
    className: `${m}-desc`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, C)))), x(/* @__PURE__ */ f.createElement("div", {
    className: ee(m, {
      [`${m}-status-${p}`]: p,
      [`${m}-type-preview`]: L,
      [`${m}-type-overview`]: !L
    }, o, E, y),
    style: s,
    ref: e
  }, F, !l && i && /* @__PURE__ */ f.createElement("button", {
    type: "button",
    className: `${m}-remove`,
    onClick: () => {
      i(n);
    }
  }, /* @__PURE__ */ f.createElement(li, null))));
}
const Nr = /* @__PURE__ */ f.forwardRef(Ys), Xn = 1;
function Zs(r) {
  const {
    prefixCls: e,
    items: t,
    onRemove: n,
    overflow: i,
    upload: o,
    listClassName: s,
    listStyle: a,
    itemClassName: c,
    itemStyle: l,
    imageProps: u
  } = r, d = `${e}-list`, h = f.useRef(null), [p, b] = f.useState(!1), {
    disabled: v
  } = f.useContext(Xe);
  f.useEffect(() => (b(!0), () => {
    b(!1);
  }), []);
  const [g, m] = f.useState(!1), [x, E] = f.useState(!1), y = () => {
    const C = h.current;
    C && (i === "scrollX" ? (m(Math.abs(C.scrollLeft) >= Xn), E(C.scrollWidth - C.clientWidth - Math.abs(C.scrollLeft) >= Xn)) : i === "scrollY" && (m(C.scrollTop !== 0), E(C.scrollHeight - C.clientHeight !== C.scrollTop)));
  };
  f.useEffect(() => {
    y();
  }, [i, t.length]);
  const _ = (C) => {
    const P = h.current;
    P && P.scrollTo({
      left: P.scrollLeft + C * P.clientWidth,
      behavior: "smooth"
    });
  }, w = () => {
    _(-1);
  }, T = () => {
    _(1);
  };
  return /* @__PURE__ */ f.createElement("div", {
    className: ee(d, {
      [`${d}-overflow-${r.overflow}`]: i,
      [`${d}-overflow-ping-start`]: g,
      [`${d}-overflow-ping-end`]: x
    }, s),
    ref: h,
    onScroll: y,
    style: a
  }, /* @__PURE__ */ f.createElement(gs, {
    keys: t.map((C) => ({
      key: C.uid,
      item: C
    })),
    motionName: `${d}-card-motion`,
    component: !1,
    motionAppear: p,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: C,
    item: P,
    className: M,
    style: D
  }) => /* @__PURE__ */ f.createElement(Nr, {
    key: C,
    prefixCls: e,
    item: P,
    onRemove: n,
    className: ee(M, c),
    imageProps: u,
    style: {
      ...D,
      ...l
    }
  })), !v && /* @__PURE__ */ f.createElement(Mr, {
    upload: o
  }, /* @__PURE__ */ f.createElement(Ie, {
    className: `${d}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ f.createElement(gi, {
    className: `${d}-upload-btn-icon`
  }))), i === "scrollX" && /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement(Ie, {
    size: "small",
    shape: "circle",
    className: `${d}-prev-btn`,
    icon: /* @__PURE__ */ f.createElement(vi, null),
    onClick: w
  }), /* @__PURE__ */ f.createElement(Ie, {
    size: "small",
    shape: "circle",
    className: `${d}-next-btn`,
    icon: /* @__PURE__ */ f.createElement(bi, null),
    onClick: T
  })));
}
function Qs(r, e) {
  const {
    prefixCls: t,
    placeholder: n = {},
    upload: i,
    className: o,
    style: s
  } = r, a = `${t}-placeholder`, c = n || {}, {
    disabled: l
  } = f.useContext(Xe), [u, d] = f.useState(!1), h = () => {
    d(!0);
  }, p = (g) => {
    g.currentTarget.contains(g.relatedTarget) || d(!1);
  }, b = () => {
    d(!1);
  }, v = /* @__PURE__ */ f.isValidElement(n) ? n : /* @__PURE__ */ f.createElement(rr, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ f.createElement(Ot.Text, {
    className: `${a}-icon`
  }, c.icon), /* @__PURE__ */ f.createElement(Ot.Title, {
    className: `${a}-title`,
    level: 5
  }, c.title), /* @__PURE__ */ f.createElement(Ot.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, c.description));
  return /* @__PURE__ */ f.createElement("div", {
    className: ee(a, {
      [`${a}-drag-in`]: u,
      [`${a}-disabled`]: l
    }, o),
    onDragEnter: h,
    onDragLeave: p,
    onDrop: b,
    "aria-hidden": l,
    style: s
  }, /* @__PURE__ */ f.createElement(nr.Dragger, ge({
    showUploadList: !1
  }, i, {
    ref: e,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), v));
}
const Js = /* @__PURE__ */ f.forwardRef(Qs);
function ea(r, e) {
  const {
    prefixCls: t,
    rootClassName: n,
    rootStyle: i,
    className: o,
    style: s,
    items: a,
    children: c,
    getDropContainer: l,
    placeholder: u,
    onChange: d,
    onRemove: h,
    overflow: p,
    imageProps: b,
    disabled: v,
    classNames: g = {},
    styles: m = {},
    ...x
  } = r, {
    getPrefixCls: E,
    direction: y
  } = Ve(), _ = E("attachment", t), w = ur("attachments"), {
    classNames: T,
    styles: C
  } = w, P = f.useRef(null), M = f.useRef(null);
  f.useImperativeHandle(e, () => ({
    nativeElement: P.current,
    upload: (j) => {
      var X, Q;
      const Z = (Q = (X = M.current) == null ? void 0 : X.nativeElement) == null ? void 0 : Q.querySelector('input[type="file"]');
      if (Z) {
        const ae = new DataTransfer();
        ae.items.add(j), Z.files = ae.files, Z.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [D, N, F] = kr(_), W = ee(N, F), [L, H] = an([], {
    value: a
  }), O = Re((j) => {
    H(j.fileList), d == null || d(j);
  }), z = {
    ...x,
    fileList: L,
    onChange: O
  }, S = (j) => Promise.resolve(typeof h == "function" ? h(j) : h).then((Z) => {
    if (Z === !1)
      return;
    const X = L.filter((Q) => Q.uid !== j.uid);
    O({
      file: {
        ...j,
        status: "removed"
      },
      fileList: X
    });
  });
  let se;
  const te = (j, Z, X) => {
    const Q = typeof u == "function" ? u(j) : u;
    return /* @__PURE__ */ f.createElement(Js, {
      placeholder: Q,
      upload: z,
      prefixCls: _,
      className: ee(T.placeholder, g.placeholder),
      style: {
        ...C.placeholder,
        ...m.placeholder,
        ...Z == null ? void 0 : Z.style
      },
      ref: X
    });
  };
  if (c)
    se = /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement(Mr, {
      upload: z,
      rootClassName: n,
      ref: M
    }, c), /* @__PURE__ */ f.createElement(Mn, {
      getDropContainer: l,
      prefixCls: _,
      className: ee(W, n)
    }, te("drop")));
  else {
    const j = L.length > 0;
    se = /* @__PURE__ */ f.createElement("div", {
      className: ee(_, W, {
        [`${_}-rtl`]: y === "rtl"
      }, o, n),
      style: {
        ...i,
        ...s
      },
      dir: y || "ltr",
      ref: P
    }, /* @__PURE__ */ f.createElement(Zs, {
      prefixCls: _,
      items: L,
      onRemove: S,
      overflow: p,
      upload: z,
      listClassName: ee(T.list, g.list),
      listStyle: {
        ...C.list,
        ...m.list,
        ...!j && {
          display: "none"
        }
      },
      itemClassName: ee(T.item, g.item),
      itemStyle: {
        ...C.item,
        ...m.item
      },
      imageProps: b
    }), te("inline", j ? {
      style: {
        display: "none"
      }
    } : {}, M), /* @__PURE__ */ f.createElement(Mn, {
      getDropContainer: l || (() => P.current),
      prefixCls: _,
      className: W
    }, te("drop")));
  }
  return D(/* @__PURE__ */ f.createElement(Xe.Provider, {
    value: {
      disabled: v
    }
  }, se));
}
const Fr = /* @__PURE__ */ f.forwardRef(ea);
Fr.FileCard = Nr;
var ta = `accept acceptCharset accessKey action allowFullScreen allowTransparency
    alt async autoComplete autoFocus autoPlay capture cellPadding cellSpacing challenge
    charSet checked classID className colSpan cols content contentEditable contextMenu
    controls coords crossOrigin data dateTime default defer dir disabled download draggable
    encType form formAction formEncType formMethod formNoValidate formTarget frameBorder
    headers height hidden high href hrefLang htmlFor httpEquiv icon id inputMode integrity
    is keyParams keyType kind label lang list loop low manifest marginHeight marginWidth max maxLength media
    mediaGroup method min minLength multiple muted name noValidate nonce open
    optimum pattern placeholder poster preload radioGroup readOnly rel required
    reversed role rowSpan rows sandbox scope scoped scrolling seamless selected
    shape size sizes span spellCheck src srcDoc srcLang srcSet start step style
    summary tabIndex target title type useMap value width wmode wrap`, na = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, ra = "".concat(ta, " ").concat(na).split(/[\s\n]+/), ia = "aria-", oa = "data-";
function Gn(r, e) {
  return r.indexOf(e) === 0;
}
function sa(r) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, t;
  e === !1 ? t = {
    aria: !0,
    data: !0,
    attr: !0
  } : e === !0 ? t = {
    aria: !0
  } : t = $({}, e);
  var n = {};
  return Object.keys(r).forEach(function(i) {
    // Aria
    (t.aria && (i === "role" || Gn(i, ia)) || // Data
    t.data && Gn(i, oa) || // Attr
    t.attr && ra.includes(i)) && (n[i] = r[i]);
  }), n;
}
function aa(r, e) {
  return Kr(r, () => {
    const t = e(), {
      nativeElement: n
    } = t;
    return new Proxy(n, {
      get(i, o) {
        return t[o] ? t[o] : Reflect.get(i, o);
      }
    });
  });
}
const Wr = /* @__PURE__ */ R.createContext({}), qn = () => ({
  height: 0
}), Kn = (r) => ({
  height: r.scrollHeight
});
function la(r) {
  const {
    title: e,
    onOpenChange: t,
    open: n,
    children: i,
    className: o,
    style: s,
    classNames: a = {},
    styles: c = {},
    closable: l,
    forceRender: u
  } = r, {
    prefixCls: d
  } = R.useContext(Wr), h = `${d}-header`;
  return /* @__PURE__ */ R.createElement(Pr, {
    motionEnter: !0,
    motionLeave: !0,
    motionName: `${h}-motion`,
    leavedClassName: `${h}-motion-hidden`,
    onEnterStart: qn,
    onEnterActive: Kn,
    onLeaveStart: Kn,
    onLeaveActive: qn,
    visible: n,
    forceRender: u
  }, ({
    className: p,
    style: b
  }) => /* @__PURE__ */ R.createElement("div", {
    className: ee(h, p, o),
    style: {
      ...b,
      ...s
    }
  }, (l !== !1 || e) && /* @__PURE__ */ R.createElement("div", {
    className: (
      // We follow antd naming standard here.
      // So the header part is use `-header` suffix.
      // Though its little bit weird for double `-header`.
      ee(`${h}-header`, a.header)
    ),
    style: {
      ...c.header
    }
  }, /* @__PURE__ */ R.createElement("div", {
    className: `${h}-title`
  }, e), l !== !1 && /* @__PURE__ */ R.createElement("div", {
    className: `${h}-close`
  }, /* @__PURE__ */ R.createElement(Ie, {
    type: "text",
    icon: /* @__PURE__ */ R.createElement(yi, null),
    size: "small",
    onClick: () => {
      t == null || t(!n);
    }
  }))), i && /* @__PURE__ */ R.createElement("div", {
    className: ee(`${h}-content`, a.content),
    style: {
      ...c.content
    }
  }, i)));
}
const Mt = /* @__PURE__ */ R.createContext(null);
function ca(r, e) {
  const {
    className: t,
    action: n,
    onClick: i,
    ...o
  } = r, s = R.useContext(Mt), {
    prefixCls: a,
    disabled: c
  } = s, l = s[n], u = c ?? o.disabled ?? s[`${n}Disabled`];
  return /* @__PURE__ */ R.createElement(Ie, ge({
    type: "text"
  }, o, {
    ref: e,
    onClick: (d) => {
      u || (l && l(), i && i(d));
    },
    className: ee(a, t, {
      [`${a}-disabled`]: u
    })
  }));
}
const Lt = /* @__PURE__ */ R.forwardRef(ca);
function ua(r, e) {
  return /* @__PURE__ */ R.createElement(Lt, ge({
    icon: /* @__PURE__ */ R.createElement(wi, null)
  }, r, {
    action: "onClear",
    ref: e
  }));
}
const da = /* @__PURE__ */ R.forwardRef(ua), fa = /* @__PURE__ */ Yr((r) => {
  const {
    className: e
  } = r;
  return /* @__PURE__ */ f.createElement("svg", {
    color: "currentColor",
    viewBox: "0 0 1000 1000",
    xmlns: "http://www.w3.org/2000/svg",
    className: e
  }, /* @__PURE__ */ f.createElement("title", null, "Stop Loading"), /* @__PURE__ */ f.createElement("rect", {
    fill: "currentColor",
    height: "250",
    rx: "24",
    ry: "24",
    width: "250",
    x: "375",
    y: "375"
  }), /* @__PURE__ */ f.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    opacity: "0.45"
  }), /* @__PURE__ */ f.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    strokeDasharray: "600 9999999"
  }, /* @__PURE__ */ f.createElement("animateTransform", {
    attributeName: "transform",
    dur: "1s",
    from: "0 500 500",
    repeatCount: "indefinite",
    to: "360 500 500",
    type: "rotate"
  })));
});
function ha(r, e) {
  const {
    prefixCls: t
  } = R.useContext(Mt), {
    className: n
  } = r;
  return /* @__PURE__ */ R.createElement(Lt, ge({
    icon: null,
    color: "primary",
    variant: "text",
    shape: "circle"
  }, r, {
    className: ee(n, `${t}-loading-button`),
    action: "onCancel",
    ref: e
  }), /* @__PURE__ */ R.createElement(fa, {
    className: `${t}-loading-icon`
  }));
}
const jr = /* @__PURE__ */ R.forwardRef(ha);
function pa(r, e) {
  return /* @__PURE__ */ R.createElement(Lt, ge({
    icon: /* @__PURE__ */ R.createElement(Si, null),
    type: "primary",
    shape: "circle"
  }, r, {
    action: "onSend",
    ref: e
  }));
}
const Br = /* @__PURE__ */ R.forwardRef(pa), je = 1e3, Be = 4, lt = 140, Yn = lt / 2, nt = 250, Zn = 500, rt = 0.8;
function ma({
  className: r
}) {
  return /* @__PURE__ */ f.createElement("svg", {
    color: "currentColor",
    viewBox: `0 0 ${je} ${je}`,
    xmlns: "http://www.w3.org/2000/svg",
    className: r
  }, /* @__PURE__ */ f.createElement("title", null, "Speech Recording"), Array.from({
    length: Be
  }).map((e, t) => {
    const n = (je - lt * Be) / (Be - 1), i = t * (n + lt), o = je / 2 - nt / 2, s = je / 2 - Zn / 2;
    return /* @__PURE__ */ f.createElement("rect", {
      fill: "currentColor",
      rx: Yn,
      ry: Yn,
      height: nt,
      width: lt,
      x: i,
      y: o,
      key: t
    }, /* @__PURE__ */ f.createElement("animate", {
      attributeName: "height",
      values: `${nt}; ${Zn}; ${nt}`,
      keyTimes: "0; 0.5; 1",
      dur: `${rt}s`,
      begin: `${rt / Be * t}s`,
      repeatCount: "indefinite"
    }), /* @__PURE__ */ f.createElement("animate", {
      attributeName: "y",
      values: `${o}; ${s}; ${o}`,
      keyTimes: "0; 0.5; 1",
      dur: `${rt}s`,
      begin: `${rt / Be * t}s`,
      repeatCount: "indefinite"
    }));
  }));
}
function ga(r, e) {
  const {
    speechRecording: t,
    onSpeechDisabled: n,
    prefixCls: i
  } = R.useContext(Mt);
  let o = null;
  return t ? o = /* @__PURE__ */ R.createElement(ma, {
    className: `${i}-recording-icon`
  }) : n ? o = /* @__PURE__ */ R.createElement(xi, null) : o = /* @__PURE__ */ R.createElement(Ci, null), /* @__PURE__ */ R.createElement(Lt, ge({
    icon: o,
    color: "primary",
    variant: "text"
  }, r, {
    action: "onSpeech",
    ref: e
  }));
}
const Hr = /* @__PURE__ */ R.forwardRef(ga), va = (r) => {
  const {
    componentCls: e,
    calc: t
  } = r, n = `${e}-header`;
  return {
    [e]: {
      [n]: {
        borderBottomWidth: r.lineWidth,
        borderBottomStyle: "solid",
        borderBottomColor: r.colorBorder,
        // ======================== Header ========================
        "&-header": {
          background: r.colorFillAlter,
          fontSize: r.fontSize,
          lineHeight: r.lineHeight,
          paddingBlock: t(r.paddingSM).sub(r.lineWidthBold).equal(),
          paddingInlineStart: r.padding,
          paddingInlineEnd: r.paddingXS,
          display: "flex",
          [`${n}-title`]: {
            flex: "auto"
          }
        },
        // ======================= Content ========================
        "&-content": {
          padding: r.padding
        },
        // ======================== Motion ========================
        "&-motion": {
          transition: ["height", "border"].map((i) => `${i} ${r.motionDurationSlow}`).join(","),
          overflow: "hidden",
          "&-enter-start, &-leave-active": {
            borderBottomColor: "transparent"
          },
          "&-hidden": {
            display: "none"
          }
        }
      }
    }
  };
}, ba = (r) => {
  const {
    componentCls: e,
    padding: t,
    paddingSM: n,
    paddingXS: i,
    paddingXXS: o,
    lineWidth: s,
    lineWidthBold: a,
    calc: c
  } = r;
  return {
    [e]: {
      position: "relative",
      width: "100%",
      boxSizing: "border-box",
      boxShadow: `${r.boxShadowTertiary}`,
      transition: `background ${r.motionDurationSlow}`,
      // Border
      borderRadius: {
        _skip_check_: !0,
        value: c(r.borderRadius).mul(2).equal()
      },
      borderColor: r.colorBorder,
      borderWidth: 0,
      borderStyle: "solid",
      // Border
      "&:after": {
        content: '""',
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        transition: `border-color ${r.motionDurationSlow}`,
        borderRadius: {
          _skip_check_: !0,
          value: "inherit"
        },
        borderStyle: "inherit",
        borderColor: "inherit",
        borderWidth: s
      },
      // Focus
      "&:focus-within": {
        boxShadow: `${r.boxShadowSecondary}`,
        borderColor: r.colorPrimary,
        "&:after": {
          borderWidth: a
        }
      },
      "&-disabled": {
        background: r.colorBgContainerDisabled
      },
      // ============================== RTL ==============================
      [`&${e}-rtl`]: {
        direction: "rtl"
      },
      // ============================ Content ============================
      [`${e}-content`]: {
        display: "flex",
        gap: i,
        width: "100%",
        paddingBlock: n,
        paddingInlineStart: t,
        paddingInlineEnd: n,
        boxSizing: "border-box",
        alignItems: "flex-end"
      },
      // ============================ Prefix =============================
      [`${e}-prefix`]: {
        flex: "none"
      },
      // ============================= Input =============================
      [`${e}-input`]: {
        padding: 0,
        borderRadius: 0,
        flex: "auto",
        alignSelf: "center",
        minHeight: "auto"
      },
      // ============================ Actions ============================
      [`${e}-actions-list`]: {
        flex: "none",
        display: "flex",
        "&-presets": {
          gap: r.paddingXS
        }
      },
      [`${e}-actions-btn`]: {
        "&-disabled": {
          opacity: 0.45
        },
        "&-loading-button": {
          padding: 0,
          border: 0
        },
        "&-loading-icon": {
          height: r.controlHeight,
          width: r.controlHeight,
          verticalAlign: "top"
        },
        "&-recording-icon": {
          height: "1.2em",
          width: "1.2em",
          verticalAlign: "top"
        }
      },
      // ============================ Footer =============================
      [`${e}-footer`]: {
        paddingInlineStart: t,
        paddingInlineEnd: n,
        paddingBlockEnd: n,
        paddingBlockStart: o,
        boxSizing: "border-box"
      }
    }
  };
}, ya = () => ({}), wa = Ir("Sender", (r) => {
  const {
    paddingXS: e,
    calc: t
  } = r, n = Pt(r, {
    SenderContentMaxWidth: `calc(100% - ${Gt(t(e).add(32).equal())})`
  });
  return [ba(n), va(n)];
}, ya);
let ht;
!ht && typeof window < "u" && (ht = window.SpeechRecognition || window.webkitSpeechRecognition);
function Sa(r, e) {
  const t = Re(r), [n, i, o] = f.useMemo(() => typeof e == "object" ? [e.recording, e.onRecordingChange, typeof e.recording == "boolean"] : [void 0, void 0, !1], [e]), [s, a] = f.useState(null);
  f.useEffect(() => {
    if (typeof navigator < "u" && "permissions" in navigator) {
      let v = null;
      return navigator.permissions.query({
        name: "microphone"
      }).then((g) => {
        a(g.state), g.onchange = function() {
          a(this.state);
        }, v = g;
      }), () => {
        v && (v.onchange = null);
      };
    }
  }, []);
  const c = ht && s !== "denied", l = f.useRef(null), [u, d] = an(!1, {
    value: n
  }), h = f.useRef(!1), p = () => {
    if (c && !l.current) {
      const v = new ht();
      v.onstart = () => {
        d(!0);
      }, v.onend = () => {
        d(!1);
      }, v.onresult = (g) => {
        var m, x, E;
        if (!h.current) {
          const y = (E = (x = (m = g.results) == null ? void 0 : m[0]) == null ? void 0 : x[0]) == null ? void 0 : E.transcript;
          t(y);
        }
        h.current = !1;
      }, l.current = v;
    }
  }, b = Re((v) => {
    v && !u || (h.current = v, o ? i == null || i(!u) : (p(), l.current && (u ? (l.current.stop(), i == null || i(!1)) : (l.current.start(), i == null || i(!0)))));
  });
  return [c, b, u];
}
function xa(r, e, t) {
  return Vo(r, e) || t;
}
const Qn = {
  SendButton: Br,
  ClearButton: da,
  LoadingButton: jr,
  SpeechButton: Hr
}, Ca = /* @__PURE__ */ f.forwardRef((r, e) => {
  const {
    prefixCls: t,
    styles: n = {},
    classNames: i = {},
    className: o,
    rootClassName: s,
    style: a,
    defaultValue: c,
    value: l,
    readOnly: u,
    submitType: d = "enter",
    onSubmit: h,
    loading: p,
    components: b,
    onCancel: v,
    onChange: g,
    actions: m,
    onKeyPress: x,
    onKeyDown: E,
    disabled: y,
    allowSpeech: _,
    prefix: w,
    footer: T,
    header: C,
    onPaste: P,
    onPasteFile: M,
    autoSize: D = {
      maxRows: 8
    },
    ...N
  } = r, {
    direction: F,
    getPrefixCls: W
  } = Ve(), L = W("sender", t), H = f.useRef(null), O = f.useRef(null);
  aa(e, () => {
    var q, ce;
    return {
      nativeElement: H.current,
      focus: (q = O.current) == null ? void 0 : q.focus,
      blur: (ce = O.current) == null ? void 0 : ce.blur
    };
  });
  const z = ur("sender"), S = `${L}-input`, [se, te, j] = wa(L), Z = ee(L, z.className, o, s, te, j, {
    [`${L}-rtl`]: F === "rtl",
    [`${L}-disabled`]: y
  }), X = `${L}-actions-btn`, Q = `${L}-actions-list`, [ae, he] = an(c || "", {
    value: l
  }), we = (q, ce) => {
    he(q), g && g(q, ce);
  }, [xe, U, A] = Sa((q) => {
    we(`${ae} ${q}`);
  }, _), B = xa(b, ["input"], Mi.TextArea), K = {
    ...sa(N, {
      attr: !0,
      aria: !0,
      data: !0
    }),
    ref: O
  }, J = () => {
    ae && h && !p && h(ae);
  }, le = () => {
    we("");
  }, fe = f.useRef(!1), G = () => {
    fe.current = !0;
  }, pe = () => {
    fe.current = !1;
  }, be = (q) => {
    const ce = q.key === "Enter" && !fe.current;
    switch (d) {
      case "enter":
        ce && !q.shiftKey && (q.preventDefault(), J());
        break;
      case "shiftEnter":
        ce && q.shiftKey && (q.preventDefault(), J());
        break;
    }
    x && x(q);
  }, I = (q) => {
    var Fe;
    const ce = (Fe = q.clipboardData) == null ? void 0 : Fe.files;
    ce != null && ce.length && M && (M(ce[0], ce), q.preventDefault()), P == null || P(q);
  }, Y = (q) => {
    var ce, Fe;
    q.target !== ((ce = H.current) == null ? void 0 : ce.querySelector(`.${S}`)) && q.preventDefault(), (Fe = O.current) == null || Fe.focus();
  };
  let ne = /* @__PURE__ */ f.createElement(rr, {
    className: `${Q}-presets`
  }, _ && /* @__PURE__ */ f.createElement(Hr, null), p ? /* @__PURE__ */ f.createElement(jr, null) : /* @__PURE__ */ f.createElement(Br, null));
  typeof m == "function" ? ne = m(ne, {
    components: Qn
  }) : (m || m === !1) && (ne = m);
  const Pe = {
    prefixCls: X,
    onSend: J,
    onSendDisabled: !ae,
    onClear: le,
    onClearDisabled: !ae,
    onCancel: v,
    onCancelDisabled: !p,
    onSpeech: () => U(!1),
    onSpeechDisabled: !xe,
    speechRecording: A,
    disabled: y
  };
  let Ce = null;
  return typeof T == "function" ? Ce = T({
    components: Qn
  }) : T && (Ce = T), se(/* @__PURE__ */ f.createElement("div", {
    ref: H,
    className: Z,
    style: {
      ...z.style,
      ...a
    }
  }, C && /* @__PURE__ */ f.createElement(Wr.Provider, {
    value: {
      prefixCls: L
    }
  }, C), /* @__PURE__ */ f.createElement(Mt.Provider, {
    value: Pe
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${L}-content`,
    onMouseDown: Y
  }, w && /* @__PURE__ */ f.createElement("div", {
    className: ee(`${L}-prefix`, z.classNames.prefix, i.prefix),
    style: {
      ...z.styles.prefix,
      ...n.prefix
    }
  }, w), /* @__PURE__ */ f.createElement(B, ge({}, K, {
    disabled: y,
    style: {
      ...z.styles.input,
      ...n.input
    },
    className: ee(S, z.classNames.input, i.input),
    autoSize: D,
    value: ae,
    onChange: (q) => {
      we(q.target.value, q), U(!0);
    },
    onPressEnter: be,
    onCompositionStart: G,
    onCompositionEnd: pe,
    onKeyDown: E,
    onPaste: I,
    variant: "borderless",
    readOnly: u
  })), ne && /* @__PURE__ */ f.createElement("div", {
    className: ee(Q, z.classNames.actions, i.actions),
    style: {
      ...z.styles.actions,
      ...n.actions
    }
  }, ne)), Ce && /* @__PURE__ */ f.createElement("div", {
    className: ee(`${L}-footer`, z.classNames.footer, i.footer),
    style: {
      ...z.styles.footer,
      ...n.footer
    }
  }, Ce))));
}), sn = Ca;
sn.Header = la;
function Ea(r) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(r.trim());
}
function _a(r, e = !1) {
  try {
    if (ni(r))
      return r;
    if (e && !Ea(r))
      return;
    if (typeof r == "string") {
      let t = r.trim();
      return t.startsWith(";") && (t = t.slice(1)), t.endsWith(";") && (t = t.slice(0, -1)), new Function(`return (...args) => (${t})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Jn(r, e) {
  return Ut(() => _a(r, e), [r, e]);
}
function ct(r) {
  const e = me(r);
  return e.current = r, Zr((...t) => {
    var n;
    return (n = e.current) == null ? void 0 : n.call(e, ...t);
  }, []);
}
function Ra({
  value: r,
  onValueChange: e
}) {
  const [t, n] = $e(r), i = me(e);
  i.current = e;
  const o = me(t);
  return o.current = t, Ee(() => {
    i.current(t);
  }, [t]), Ee(() => {
    qi(r, o.current) || n(r);
  }, [r]), [t, n];
}
function Ta(r, e) {
  return Object.keys(r).reduce((t, n) => (r[n] !== void 0 && r[n] !== null && (t[n] = r[n]), t), {});
}
function Ht(r, e, t, n) {
  return new (t || (t = Promise))(function(i, o) {
    function s(l) {
      try {
        c(n.next(l));
      } catch (u) {
        o(u);
      }
    }
    function a(l) {
      try {
        c(n.throw(l));
      } catch (u) {
        o(u);
      }
    }
    function c(l) {
      var u;
      l.done ? i(l.value) : (u = l.value, u instanceof t ? u : new t(function(d) {
        d(u);
      })).then(s, a);
    }
    c((n = n.apply(r, [])).next());
  });
}
class zr {
  constructor() {
    this.listeners = {};
  }
  on(e, t, n) {
    if (this.listeners[e] || (this.listeners[e] = /* @__PURE__ */ new Set()), this.listeners[e].add(t), n == null ? void 0 : n.once) {
      const i = () => {
        this.un(e, i), this.un(e, t);
      };
      return this.on(e, i), i;
    }
    return () => this.un(e, t);
  }
  un(e, t) {
    var n;
    (n = this.listeners[e]) === null || n === void 0 || n.delete(t);
  }
  once(e, t) {
    return this.on(e, t, {
      once: !0
    });
  }
  unAll() {
    this.listeners = {};
  }
  emit(e, ...t) {
    this.listeners[e] && this.listeners[e].forEach((n) => n(...t));
  }
}
class Pa extends zr {
  constructor(e) {
    super(), this.subscriptions = [], this.options = e;
  }
  onInit() {
  }
  _init(e) {
    this.wavesurfer = e, this.onInit();
  }
  destroy() {
    this.emit("destroy"), this.subscriptions.forEach((e) => e());
  }
}
class Ma extends zr {
  constructor() {
    super(...arguments), this.unsubscribe = () => {
    };
  }
  start() {
    this.unsubscribe = this.on("tick", () => {
      requestAnimationFrame(() => {
        this.emit("tick");
      });
    }), this.emit("tick");
  }
  stop() {
    this.unsubscribe();
  }
  destroy() {
    this.unsubscribe();
  }
}
const La = ["audio/webm", "audio/wav", "audio/mpeg", "audio/mp4", "audio/mp3"];
class fn extends Pa {
  constructor(e) {
    var t, n, i, o, s, a;
    super(Object.assign(Object.assign({}, e), {
      audioBitsPerSecond: (t = e.audioBitsPerSecond) !== null && t !== void 0 ? t : 128e3,
      scrollingWaveform: (n = e.scrollingWaveform) !== null && n !== void 0 && n,
      scrollingWaveformWindow: (i = e.scrollingWaveformWindow) !== null && i !== void 0 ? i : 5,
      continuousWaveform: (o = e.continuousWaveform) !== null && o !== void 0 && o,
      renderRecordedAudio: (s = e.renderRecordedAudio) === null || s === void 0 || s,
      mediaRecorderTimeslice: (a = e.mediaRecorderTimeslice) !== null && a !== void 0 ? a : void 0
    })), this.stream = null, this.mediaRecorder = null, this.dataWindow = null, this.isWaveformPaused = !1, this.lastStartTime = 0, this.lastDuration = 0, this.duration = 0, this.timer = new Ma(), this.subscriptions.push(this.timer.on("tick", () => {
      const c = performance.now() - this.lastStartTime;
      this.duration = this.isPaused() ? this.duration : this.lastDuration + c, this.emit("record-progress", this.duration);
    }));
  }
  static create(e) {
    return new fn(e || {});
  }
  renderMicStream(e) {
    var t;
    const n = new AudioContext(), i = n.createMediaStreamSource(e), o = n.createAnalyser();
    i.connect(o), this.options.continuousWaveform && (o.fftSize = 32);
    const s = o.frequencyBinCount, a = new Float32Array(s);
    let c = 0;
    this.wavesurfer && ((t = this.originalOptions) !== null && t !== void 0 || (this.originalOptions = Object.assign({}, this.wavesurfer.options)), this.wavesurfer.options.interact = !1, this.options.scrollingWaveform && (this.wavesurfer.options.cursorWidth = 0));
    const l = setInterval(() => {
      var u, d, h, p;
      if (!this.isWaveformPaused) {
        if (o.getFloatTimeDomainData(a), this.options.scrollingWaveform) {
          const b = Math.floor((this.options.scrollingWaveformWindow || 0) * n.sampleRate), v = Math.min(b, this.dataWindow ? this.dataWindow.length + s : s), g = new Float32Array(b);
          if (this.dataWindow) {
            const m = Math.max(0, b - this.dataWindow.length);
            g.set(this.dataWindow.slice(-v + s), m);
          }
          g.set(a, b - s), this.dataWindow = g;
        } else if (this.options.continuousWaveform) {
          if (!this.dataWindow) {
            const v = this.options.continuousWaveformDuration ? Math.round(100 * this.options.continuousWaveformDuration) : ((d = (u = this.wavesurfer) === null || u === void 0 ? void 0 : u.getWidth()) !== null && d !== void 0 ? d : 0) * window.devicePixelRatio;
            this.dataWindow = new Float32Array(v);
          }
          let b = 0;
          for (let v = 0; v < s; v++) {
            const g = Math.abs(a[v]);
            g > b && (b = g);
          }
          if (c + 1 > this.dataWindow.length) {
            const v = new Float32Array(2 * this.dataWindow.length);
            v.set(this.dataWindow, 0), this.dataWindow = v;
          }
          this.dataWindow[c] = b, c++;
        } else this.dataWindow = a;
        if (this.wavesurfer) {
          const b = ((p = (h = this.dataWindow) === null || h === void 0 ? void 0 : h.length) !== null && p !== void 0 ? p : 0) / 100;
          this.wavesurfer.load("", [this.dataWindow], this.options.scrollingWaveform ? this.options.scrollingWaveformWindow : b).then(() => {
            this.wavesurfer && this.options.continuousWaveform && (this.wavesurfer.setTime(this.getDuration() / 1e3), this.wavesurfer.options.minPxPerSec || this.wavesurfer.setOptions({
              minPxPerSec: this.wavesurfer.getWidth() / this.wavesurfer.getDuration()
            }));
          }).catch((v) => {
            console.error("Error rendering real-time recording data:", v);
          });
        }
      }
    }, 10);
    return {
      onDestroy: () => {
        clearInterval(l), i == null || i.disconnect(), n == null || n.close();
      },
      onEnd: () => {
        this.isWaveformPaused = !0, clearInterval(l), this.stopMic();
      }
    };
  }
  startMic(e) {
    return Ht(this, void 0, void 0, function* () {
      let t;
      try {
        t = yield navigator.mediaDevices.getUserMedia({
          audio: !(e != null && e.deviceId) || {
            deviceId: e.deviceId
          }
        });
      } catch (o) {
        throw new Error("Error accessing the microphone: " + o.message);
      }
      const {
        onDestroy: n,
        onEnd: i
      } = this.renderMicStream(t);
      return this.subscriptions.push(this.once("destroy", n)), this.subscriptions.push(this.once("record-end", i)), this.stream = t, t;
    });
  }
  stopMic() {
    this.stream && (this.stream.getTracks().forEach((e) => e.stop()), this.stream = null, this.mediaRecorder = null);
  }
  startRecording(e) {
    return Ht(this, void 0, void 0, function* () {
      const t = this.stream || (yield this.startMic(e));
      this.dataWindow = null;
      const n = this.mediaRecorder || new MediaRecorder(t, {
        mimeType: this.options.mimeType || La.find((s) => MediaRecorder.isTypeSupported(s)),
        audioBitsPerSecond: this.options.audioBitsPerSecond
      });
      this.mediaRecorder = n, this.stopRecording();
      const i = [];
      n.ondataavailable = (s) => {
        s.data.size > 0 && i.push(s.data), this.emit("record-data-available", s.data);
      };
      const o = (s) => {
        var a;
        const c = new Blob(i, {
          type: n.mimeType
        });
        this.emit(s, c), this.options.renderRecordedAudio && (this.applyOriginalOptionsIfNeeded(), (a = this.wavesurfer) === null || a === void 0 || a.load(URL.createObjectURL(c)));
      };
      n.onpause = () => o("record-pause"), n.onstop = () => o("record-end"), n.start(this.options.mediaRecorderTimeslice), this.lastStartTime = performance.now(), this.lastDuration = 0, this.duration = 0, this.isWaveformPaused = !1, this.timer.start(), this.emit("record-start");
    });
  }
  getDuration() {
    return this.duration;
  }
  isRecording() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) === "recording";
  }
  isPaused() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) === "paused";
  }
  isActive() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) !== "inactive";
  }
  stopRecording() {
    var e;
    this.isActive() && ((e = this.mediaRecorder) === null || e === void 0 || e.stop(), this.timer.stop());
  }
  pauseRecording() {
    var e, t;
    this.isRecording() && (this.isWaveformPaused = !0, (e = this.mediaRecorder) === null || e === void 0 || e.requestData(), (t = this.mediaRecorder) === null || t === void 0 || t.pause(), this.timer.stop(), this.lastDuration = this.duration);
  }
  resumeRecording() {
    var e;
    this.isPaused() && (this.isWaveformPaused = !1, (e = this.mediaRecorder) === null || e === void 0 || e.resume(), this.timer.start(), this.lastStartTime = performance.now(), this.emit("record-resume"));
  }
  static getAvailableAudioDevices() {
    return Ht(this, void 0, void 0, function* () {
      return navigator.mediaDevices.enumerateDevices().then((e) => e.filter((t) => t.kind === "audioinput"));
    });
  }
  destroy() {
    this.applyOriginalOptionsIfNeeded(), super.destroy(), this.stopRecording(), this.stopMic();
  }
  applyOriginalOptionsIfNeeded() {
    this.wavesurfer && this.originalOptions && (this.wavesurfer.setOptions(this.originalOptions), delete this.originalOptions);
  }
}
class Ge {
  constructor() {
    this.listeners = {};
  }
  /** Subscribe to an event. Returns an unsubscribe function. */
  on(e, t, n) {
    if (this.listeners[e] || (this.listeners[e] = /* @__PURE__ */ new Set()), this.listeners[e].add(t), n != null && n.once) {
      const i = () => {
        this.un(e, i), this.un(e, t);
      };
      return this.on(e, i), i;
    }
    return () => this.un(e, t);
  }
  /** Unsubscribe from an event */
  un(e, t) {
    var n;
    (n = this.listeners[e]) === null || n === void 0 || n.delete(t);
  }
  /** Subscribe to an event only once */
  once(e, t) {
    return this.on(e, t, {
      once: !0
    });
  }
  /** Clear all events */
  unAll() {
    this.listeners = {};
  }
  /** Emit an event */
  emit(e, ...t) {
    this.listeners[e] && this.listeners[e].forEach((n) => n(...t));
  }
}
class Oa extends Ge {
  /** Create a plugin instance */
  constructor(e) {
    super(), this.subscriptions = [], this.options = e;
  }
  /** Called after this.wavesurfer is available */
  onInit() {
  }
  /** Do not call directly, only called by WavesSurfer internally */
  _init(e) {
    this.wavesurfer = e, this.onInit();
  }
  /** Destroy the plugin and unsubscribe from all events */
  destroy() {
    this.emit("destroy"), this.subscriptions.forEach((e) => e());
  }
}
var Aa = function(r, e, t, n) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(n.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(n.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((n = n.apply(r, e || [])).next());
  });
};
function $a(r, e) {
  return Aa(this, void 0, void 0, function* () {
    const t = new AudioContext({
      sampleRate: e
    });
    return t.decodeAudioData(r).finally(() => t.close());
  });
}
function Ia(r) {
  const e = r[0];
  if (e.some((t) => t > 1 || t < -1)) {
    const t = e.length;
    let n = 0;
    for (let i = 0; i < t; i++) {
      const o = Math.abs(e[i]);
      o > n && (n = o);
    }
    for (const i of r)
      for (let o = 0; o < t; o++)
        i[o] /= n;
  }
  return r;
}
function ka(r, e) {
  return typeof r[0] == "number" && (r = [r]), Ia(r), {
    duration: e,
    length: r[0].length,
    sampleRate: r[0].length / e,
    numberOfChannels: r.length,
    getChannelData: (t) => r == null ? void 0 : r[t],
    copyFromChannel: AudioBuffer.prototype.copyFromChannel,
    copyToChannel: AudioBuffer.prototype.copyToChannel
  };
}
const it = {
  decode: $a,
  createBuffer: ka
};
function Vr(r, e) {
  const t = e.xmlns ? document.createElementNS(e.xmlns, r) : document.createElement(r);
  for (const [n, i] of Object.entries(e))
    if (n === "children")
      for (const [o, s] of Object.entries(e))
        typeof s == "string" ? t.appendChild(document.createTextNode(s)) : t.appendChild(Vr(o, s));
    else n === "style" ? Object.assign(t.style, i) : n === "textContent" ? t.textContent = i : t.setAttribute(n, i.toString());
  return t;
}
function er(r, e, t) {
  const n = Vr(r, e || {});
  return t == null || t.appendChild(n), n;
}
const Da = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  createElement: er,
  default: er
}, Symbol.toStringTag, {
  value: "Module"
}));
var ut = function(r, e, t, n) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(n.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(n.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((n = n.apply(r, e || [])).next());
  });
};
function Na(r, e) {
  return ut(this, void 0, void 0, function* () {
    if (!r.body || !r.headers) return;
    const t = r.body.getReader(), n = Number(r.headers.get("Content-Length")) || 0;
    let i = 0;
    const o = (a) => ut(this, void 0, void 0, function* () {
      i += (a == null ? void 0 : a.length) || 0;
      const c = Math.round(i / n * 100);
      e(c);
    }), s = () => ut(this, void 0, void 0, function* () {
      let a;
      try {
        a = yield t.read();
      } catch {
        return;
      }
      a.done || (o(a.value), yield s());
    });
    s();
  });
}
function Fa(r, e, t) {
  return ut(this, void 0, void 0, function* () {
    const n = yield fetch(r, t);
    if (n.status >= 400)
      throw new Error(`Failed to fetch ${r}: ${n.status} (${n.statusText})`);
    return Na(n.clone(), e), n.blob();
  });
}
const Wa = {
  fetchBlob: Fa
};
var ja = function(r, e, t, n) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(n.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(n.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((n = n.apply(r, e || [])).next());
  });
};
class Ba extends Ge {
  constructor(e) {
    super(), this.isExternalMedia = !1, e.media ? (this.media = e.media, this.isExternalMedia = !0) : this.media = document.createElement("audio"), e.mediaControls && (this.media.controls = !0), e.autoplay && (this.media.autoplay = !0), e.playbackRate != null && this.onMediaEvent("canplay", () => {
      e.playbackRate != null && (this.media.playbackRate = e.playbackRate);
    }, {
      once: !0
    });
  }
  onMediaEvent(e, t, n) {
    return this.media.addEventListener(e, t, n), () => this.media.removeEventListener(e, t, n);
  }
  getSrc() {
    return this.media.currentSrc || this.media.src || "";
  }
  revokeSrc() {
    const e = this.getSrc();
    e.startsWith("blob:") && URL.revokeObjectURL(e);
  }
  canPlayType(e) {
    return this.media.canPlayType(e) !== "";
  }
  setSrc(e, t) {
    const n = this.getSrc();
    if (e && n === e) return;
    this.revokeSrc();
    const i = t instanceof Blob && (this.canPlayType(t.type) || !e) ? URL.createObjectURL(t) : e;
    n && (this.media.src = "");
    try {
      this.media.src = i;
    } catch {
      this.media.src = e;
    }
  }
  destroy() {
    this.isExternalMedia || (this.media.pause(), this.media.remove(), this.revokeSrc(), this.media.src = "", this.media.load());
  }
  setMediaElement(e) {
    this.media = e;
  }
  /** Start playing the audio */
  play() {
    return ja(this, void 0, void 0, function* () {
      return this.media.play();
    });
  }
  /** Pause the audio */
  pause() {
    this.media.pause();
  }
  /** Check if the audio is playing */
  isPlaying() {
    return !this.media.paused && !this.media.ended;
  }
  /** Jump to a specific time in the audio (in seconds) */
  setTime(e) {
    this.media.currentTime = Math.max(0, Math.min(e, this.getDuration()));
  }
  /** Get the duration of the audio in seconds */
  getDuration() {
    return this.media.duration;
  }
  /** Get the current audio position in seconds */
  getCurrentTime() {
    return this.media.currentTime;
  }
  /** Get the audio volume */
  getVolume() {
    return this.media.volume;
  }
  /** Set the audio volume */
  setVolume(e) {
    this.media.volume = e;
  }
  /** Get the audio muted state */
  getMuted() {
    return this.media.muted;
  }
  /** Mute or unmute the audio */
  setMuted(e) {
    this.media.muted = e;
  }
  /** Get the playback speed */
  getPlaybackRate() {
    return this.media.playbackRate;
  }
  /** Check if the audio is seeking */
  isSeeking() {
    return this.media.seeking;
  }
  /** Set the playback speed, pass an optional false to NOT preserve the pitch */
  setPlaybackRate(e, t) {
    t != null && (this.media.preservesPitch = t), this.media.playbackRate = e;
  }
  /** Get the HTML media element */
  getMediaElement() {
    return this.media;
  }
  /** Set a sink id to change the audio output device */
  setSinkId(e) {
    return this.media.setSinkId(e);
  }
}
function Ha(r, e, t, n, i = 3, o = 0, s = 100) {
  if (!r) return () => {
  };
  const a = matchMedia("(pointer: coarse)").matches;
  let c = () => {
  };
  const l = (u) => {
    if (u.button !== o) return;
    u.preventDefault(), u.stopPropagation();
    let d = u.clientX, h = u.clientY, p = !1;
    const b = Date.now(), v = (y) => {
      if (y.preventDefault(), y.stopPropagation(), a && Date.now() - b < s) return;
      const _ = y.clientX, w = y.clientY, T = _ - d, C = w - h;
      if (p || Math.abs(T) > i || Math.abs(C) > i) {
        const P = r.getBoundingClientRect(), {
          left: M,
          top: D
        } = P;
        p || (t == null || t(d - M, h - D), p = !0), e(T, C, _ - M, w - D), d = _, h = w;
      }
    }, g = (y) => {
      if (p) {
        const _ = y.clientX, w = y.clientY, T = r.getBoundingClientRect(), {
          left: C,
          top: P
        } = T;
        n == null || n(_ - C, w - P);
      }
      c();
    }, m = (y) => {
      (!y.relatedTarget || y.relatedTarget === document.documentElement) && g(y);
    }, x = (y) => {
      p && (y.stopPropagation(), y.preventDefault());
    }, E = (y) => {
      p && y.preventDefault();
    };
    document.addEventListener("pointermove", v), document.addEventListener("pointerup", g), document.addEventListener("pointerout", m), document.addEventListener("pointercancel", m), document.addEventListener("touchmove", E, {
      passive: !1
    }), document.addEventListener("click", x, {
      capture: !0
    }), c = () => {
      document.removeEventListener("pointermove", v), document.removeEventListener("pointerup", g), document.removeEventListener("pointerout", m), document.removeEventListener("pointercancel", m), document.removeEventListener("touchmove", E), setTimeout(() => {
        document.removeEventListener("click", x, {
          capture: !0
        });
      }, 10);
    };
  };
  return r.addEventListener("pointerdown", l), () => {
    c(), r.removeEventListener("pointerdown", l);
  };
}
var tr = function(r, e, t, n) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(n.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(n.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((n = n.apply(r, e || [])).next());
  });
}, za = function(r, e) {
  var t = {};
  for (var n in r) Object.prototype.hasOwnProperty.call(r, n) && e.indexOf(n) < 0 && (t[n] = r[n]);
  if (r != null && typeof Object.getOwnPropertySymbols == "function") for (var i = 0, n = Object.getOwnPropertySymbols(r); i < n.length; i++)
    e.indexOf(n[i]) < 0 && Object.prototype.propertyIsEnumerable.call(r, n[i]) && (t[n[i]] = r[n[i]]);
  return t;
};
class ke extends Ge {
  constructor(e, t) {
    super(), this.timeouts = [], this.isScrollable = !1, this.audioData = null, this.resizeObserver = null, this.lastContainerWidth = 0, this.isDragging = !1, this.subscriptions = [], this.unsubscribeOnScroll = [], this.subscriptions = [], this.options = e;
    const n = this.parentFromOptionsContainer(e.container);
    this.parent = n;
    const [i, o] = this.initHtml();
    n.appendChild(i), this.container = i, this.scrollContainer = o.querySelector(".scroll"), this.wrapper = o.querySelector(".wrapper"), this.canvasWrapper = o.querySelector(".canvases"), this.progressWrapper = o.querySelector(".progress"), this.cursor = o.querySelector(".cursor"), t && o.appendChild(t), this.initEvents();
  }
  parentFromOptionsContainer(e) {
    let t;
    if (typeof e == "string" ? t = document.querySelector(e) : e instanceof HTMLElement && (t = e), !t)
      throw new Error("Container not found");
    return t;
  }
  initEvents() {
    const e = (t) => {
      const n = this.wrapper.getBoundingClientRect(), i = t.clientX - n.left, o = t.clientY - n.top, s = i / n.width, a = o / n.height;
      return [s, a];
    };
    if (this.wrapper.addEventListener("click", (t) => {
      const [n, i] = e(t);
      this.emit("click", n, i);
    }), this.wrapper.addEventListener("dblclick", (t) => {
      const [n, i] = e(t);
      this.emit("dblclick", n, i);
    }), (this.options.dragToSeek === !0 || typeof this.options.dragToSeek == "object") && this.initDrag(), this.scrollContainer.addEventListener("scroll", () => {
      const {
        scrollLeft: t,
        scrollWidth: n,
        clientWidth: i
      } = this.scrollContainer, o = t / n, s = (t + i) / n;
      this.emit("scroll", o, s, t, t + i);
    }), typeof ResizeObserver == "function") {
      const t = this.createDelay(100);
      this.resizeObserver = new ResizeObserver(() => {
        t().then(() => this.onContainerResize()).catch(() => {
        });
      }), this.resizeObserver.observe(this.scrollContainer);
    }
  }
  onContainerResize() {
    const e = this.parent.clientWidth;
    e === this.lastContainerWidth && this.options.height !== "auto" || (this.lastContainerWidth = e, this.reRender());
  }
  initDrag() {
    this.subscriptions.push(Ha(
      this.wrapper,
      // On drag
      (e, t, n) => {
        this.emit("drag", Math.max(0, Math.min(1, n / this.wrapper.getBoundingClientRect().width)));
      },
      // On start drag
      (e) => {
        this.isDragging = !0, this.emit("dragstart", Math.max(0, Math.min(1, e / this.wrapper.getBoundingClientRect().width)));
      },
      // On end drag
      (e) => {
        this.isDragging = !1, this.emit("dragend", Math.max(0, Math.min(1, e / this.wrapper.getBoundingClientRect().width)));
      }
    ));
  }
  getHeight(e, t) {
    var n;
    const o = ((n = this.audioData) === null || n === void 0 ? void 0 : n.numberOfChannels) || 1;
    if (e == null) return 128;
    if (!isNaN(Number(e))) return Number(e);
    if (e === "auto") {
      const s = this.parent.clientHeight || 128;
      return t != null && t.every((a) => !a.overlay) ? s / o : s;
    }
    return 128;
  }
  initHtml() {
    const e = document.createElement("div"), t = e.attachShadow({
      mode: "open"
    }), n = this.options.cspNonce && typeof this.options.cspNonce == "string" ? this.options.cspNonce.replace(/"/g, "") : "";
    return t.innerHTML = `
      <style${n ? ` nonce="${n}"` : ""}>
        :host {
          user-select: none;
          min-width: 1px;
        }
        :host audio {
          display: block;
          width: 100%;
        }
        :host .scroll {
          overflow-x: auto;
          overflow-y: hidden;
          width: 100%;
          position: relative;
        }
        :host .noScrollbar {
          scrollbar-color: transparent;
          scrollbar-width: none;
        }
        :host .noScrollbar::-webkit-scrollbar {
          display: none;
          -webkit-appearance: none;
        }
        :host .wrapper {
          position: relative;
          overflow: visible;
          z-index: 2;
        }
        :host .canvases {
          min-height: ${this.getHeight(this.options.height, this.options.splitChannels)}px;
        }
        :host .canvases > div {
          position: relative;
        }
        :host canvas {
          display: block;
          position: absolute;
          top: 0;
          image-rendering: pixelated;
        }
        :host .progress {
          pointer-events: none;
          position: absolute;
          z-index: 2;
          top: 0;
          left: 0;
          width: 0;
          height: 100%;
          overflow: hidden;
        }
        :host .progress > div {
          position: relative;
        }
        :host .cursor {
          pointer-events: none;
          position: absolute;
          z-index: 5;
          top: 0;
          left: 0;
          height: 100%;
          border-radius: 2px;
        }
      </style>

      <div class="scroll" part="scroll">
        <div class="wrapper" part="wrapper">
          <div class="canvases" part="canvases"></div>
          <div class="progress" part="progress"></div>
          <div class="cursor" part="cursor"></div>
        </div>
      </div>
    `, [e, t];
  }
  /** Wavesurfer itself calls this method. Do not call it manually. */
  setOptions(e) {
    if (this.options.container !== e.container) {
      const t = this.parentFromOptionsContainer(e.container);
      t.appendChild(this.container), this.parent = t;
    }
    (e.dragToSeek === !0 || typeof this.options.dragToSeek == "object") && this.initDrag(), this.options = e, this.reRender();
  }
  getWrapper() {
    return this.wrapper;
  }
  getWidth() {
    return this.scrollContainer.clientWidth;
  }
  getScroll() {
    return this.scrollContainer.scrollLeft;
  }
  setScroll(e) {
    this.scrollContainer.scrollLeft = e;
  }
  setScrollPercentage(e) {
    const {
      scrollWidth: t
    } = this.scrollContainer, n = t * e;
    this.setScroll(n);
  }
  destroy() {
    var e, t;
    this.subscriptions.forEach((n) => n()), this.container.remove(), (e = this.resizeObserver) === null || e === void 0 || e.disconnect(), (t = this.unsubscribeOnScroll) === null || t === void 0 || t.forEach((n) => n()), this.unsubscribeOnScroll = [];
  }
  createDelay(e = 10) {
    let t, n;
    const i = () => {
      t && clearTimeout(t), n && n();
    };
    return this.timeouts.push(i), () => new Promise((o, s) => {
      i(), n = s, t = setTimeout(() => {
        t = void 0, n = void 0, o();
      }, e);
    });
  }
  // Convert array of color values to linear gradient
  convertColorValues(e) {
    if (!Array.isArray(e)) return e || "";
    if (e.length < 2) return e[0] || "";
    const t = document.createElement("canvas"), n = t.getContext("2d"), i = t.height * (window.devicePixelRatio || 1), o = n.createLinearGradient(0, 0, 0, i), s = 1 / (e.length - 1);
    return e.forEach((a, c) => {
      const l = c * s;
      o.addColorStop(l, a);
    }), o;
  }
  getPixelRatio() {
    return Math.max(1, window.devicePixelRatio || 1);
  }
  renderBarWaveform(e, t, n, i) {
    const o = e[0], s = e[1] || e[0], a = o.length, {
      width: c,
      height: l
    } = n.canvas, u = l / 2, d = this.getPixelRatio(), h = t.barWidth ? t.barWidth * d : 1, p = t.barGap ? t.barGap * d : t.barWidth ? h / 2 : 0, b = t.barRadius || 0, v = c / (h + p) / a, g = b && "roundRect" in n ? "roundRect" : "rect";
    n.beginPath();
    let m = 0, x = 0, E = 0;
    for (let y = 0; y <= a; y++) {
      const _ = Math.round(y * v);
      if (_ > m) {
        const C = Math.round(x * u * i), P = Math.round(E * u * i), M = C + P || 1;
        let D = u - C;
        t.barAlign === "top" ? D = 0 : t.barAlign === "bottom" && (D = l - M), n[g](m * (h + p), D, h, M, b), m = _, x = 0, E = 0;
      }
      const w = Math.abs(o[y] || 0), T = Math.abs(s[y] || 0);
      w > x && (x = w), T > E && (E = T);
    }
    n.fill(), n.closePath();
  }
  renderLineWaveform(e, t, n, i) {
    const o = (s) => {
      const a = e[s] || e[0], c = a.length, {
        height: l
      } = n.canvas, u = l / 2, d = n.canvas.width / c;
      n.moveTo(0, u);
      let h = 0, p = 0;
      for (let b = 0; b <= c; b++) {
        const v = Math.round(b * d);
        if (v > h) {
          const m = Math.round(p * u * i) || 1, x = u + m * (s === 0 ? -1 : 1);
          n.lineTo(h, x), h = v, p = 0;
        }
        const g = Math.abs(a[b] || 0);
        g > p && (p = g);
      }
      n.lineTo(h, u);
    };
    n.beginPath(), o(0), o(1), n.fill(), n.closePath();
  }
  renderWaveform(e, t, n) {
    if (n.fillStyle = this.convertColorValues(t.waveColor), t.renderFunction) {
      t.renderFunction(e, n);
      return;
    }
    let i = t.barHeight || 1;
    if (t.normalize) {
      const o = Array.from(e[0]).reduce((s, a) => Math.max(s, Math.abs(a)), 0);
      i = o ? 1 / o : 1;
    }
    if (t.barWidth || t.barGap || t.barAlign) {
      this.renderBarWaveform(e, t, n, i);
      return;
    }
    this.renderLineWaveform(e, t, n, i);
  }
  renderSingleCanvas(e, t, n, i, o, s, a) {
    const c = this.getPixelRatio(), l = document.createElement("canvas");
    l.width = Math.round(n * c), l.height = Math.round(i * c), l.style.width = `${n}px`, l.style.height = `${i}px`, l.style.left = `${Math.round(o)}px`, s.appendChild(l);
    const u = l.getContext("2d");
    if (this.renderWaveform(e, t, u), l.width > 0 && l.height > 0) {
      const d = l.cloneNode(), h = d.getContext("2d");
      h.drawImage(l, 0, 0), h.globalCompositeOperation = "source-in", h.fillStyle = this.convertColorValues(t.progressColor), h.fillRect(0, 0, l.width, l.height), a.appendChild(d);
    }
  }
  renderMultiCanvas(e, t, n, i, o, s) {
    const a = this.getPixelRatio(), {
      clientWidth: c
    } = this.scrollContainer, l = n / a;
    let u = Math.min(ke.MAX_CANVAS_WIDTH, c, l), d = {};
    if (u === 0) return;
    if (t.barWidth || t.barGap) {
      const m = t.barWidth || 0.5, x = t.barGap || m / 2, E = m + x;
      u % E !== 0 && (u = Math.floor(u / E) * E);
    }
    const h = (m) => {
      if (m < 0 || m >= b || d[m]) return;
      d[m] = !0;
      const x = m * u, E = Math.min(l - x, u);
      if (E <= 0) return;
      const y = e.map((_) => {
        const w = Math.floor(x / l * _.length), T = Math.floor((x + E) / l * _.length);
        return _.slice(w, T);
      });
      this.renderSingleCanvas(y, t, E, i, x, o, s);
    }, p = () => {
      Object.keys(d).length > ke.MAX_NODES && (o.innerHTML = "", s.innerHTML = "", d = {});
    }, b = Math.ceil(l / u);
    if (!this.isScrollable) {
      for (let m = 0; m < b; m++)
        h(m);
      return;
    }
    const v = this.scrollContainer.scrollLeft / l, g = Math.floor(v * b);
    if (h(g - 1), h(g), h(g + 1), b > 1) {
      const m = this.on("scroll", () => {
        const {
          scrollLeft: x
        } = this.scrollContainer, E = Math.floor(x / l * b);
        p(), h(E - 1), h(E), h(E + 1);
      });
      this.unsubscribeOnScroll.push(m);
    }
  }
  renderChannel(e, t, n, i) {
    var {
      overlay: o
    } = t, s = za(t, ["overlay"]);
    const a = document.createElement("div"), c = this.getHeight(s.height, s.splitChannels);
    a.style.height = `${c}px`, o && i > 0 && (a.style.marginTop = `-${c}px`), this.canvasWrapper.style.minHeight = `${c}px`, this.canvasWrapper.appendChild(a);
    const l = a.cloneNode();
    this.progressWrapper.appendChild(l), this.renderMultiCanvas(e, s, n, c, a, l);
  }
  render(e) {
    return tr(this, void 0, void 0, function* () {
      var t;
      this.timeouts.forEach((c) => c()), this.timeouts = [], this.canvasWrapper.innerHTML = "", this.progressWrapper.innerHTML = "", this.options.width != null && (this.scrollContainer.style.width = typeof this.options.width == "number" ? `${this.options.width}px` : this.options.width);
      const n = this.getPixelRatio(), i = this.scrollContainer.clientWidth, o = Math.ceil(e.duration * (this.options.minPxPerSec || 0));
      this.isScrollable = o > i;
      const s = this.options.fillParent && !this.isScrollable, a = (s ? i : o) * n;
      if (this.wrapper.style.width = s ? "100%" : `${o}px`, this.scrollContainer.style.overflowX = this.isScrollable ? "auto" : "hidden", this.scrollContainer.classList.toggle("noScrollbar", !!this.options.hideScrollbar), this.cursor.style.backgroundColor = `${this.options.cursorColor || this.options.progressColor}`, this.cursor.style.width = `${this.options.cursorWidth}px`, this.audioData = e, this.emit("render"), this.options.splitChannels)
        for (let c = 0; c < e.numberOfChannels; c++) {
          const l = Object.assign(Object.assign({}, this.options), (t = this.options.splitChannels) === null || t === void 0 ? void 0 : t[c]);
          this.renderChannel([e.getChannelData(c)], l, a, c);
        }
      else {
        const c = [e.getChannelData(0)];
        e.numberOfChannels > 1 && c.push(e.getChannelData(1)), this.renderChannel(c, this.options, a, 0);
      }
      Promise.resolve().then(() => this.emit("rendered"));
    });
  }
  reRender() {
    if (this.unsubscribeOnScroll.forEach((n) => n()), this.unsubscribeOnScroll = [], !this.audioData) return;
    const {
      scrollWidth: e
    } = this.scrollContainer, {
      right: t
    } = this.progressWrapper.getBoundingClientRect();
    if (this.render(this.audioData), this.isScrollable && e !== this.scrollContainer.scrollWidth) {
      const {
        right: n
      } = this.progressWrapper.getBoundingClientRect();
      let i = n - t;
      i *= 2, i = i < 0 ? Math.floor(i) : Math.ceil(i), i /= 2, this.scrollContainer.scrollLeft += i;
    }
  }
  zoom(e) {
    this.options.minPxPerSec = e, this.reRender();
  }
  scrollIntoView(e, t = !1) {
    const {
      scrollLeft: n,
      scrollWidth: i,
      clientWidth: o
    } = this.scrollContainer, s = e * i, a = n, c = n + o, l = o / 2;
    if (this.isDragging)
      s + 30 > c ? this.scrollContainer.scrollLeft += 30 : s - 30 < a && (this.scrollContainer.scrollLeft -= 30);
    else {
      (s < a || s > c) && (this.scrollContainer.scrollLeft = s - (this.options.autoCenter ? l : 0));
      const u = s - n - l;
      t && this.options.autoCenter && u > 0 && (this.scrollContainer.scrollLeft += Math.min(u, 10));
    }
    {
      const u = this.scrollContainer.scrollLeft, d = u / i, h = (u + o) / i;
      this.emit("scroll", d, h, u, u + o);
    }
  }
  renderProgress(e, t) {
    if (isNaN(e)) return;
    const n = e * 100;
    this.canvasWrapper.style.clipPath = `polygon(${n}% 0, 100% 0, 100% 100%, ${n}% 100%)`, this.progressWrapper.style.width = `${n}%`, this.cursor.style.left = `${n}%`, this.cursor.style.transform = `translateX(-${Math.round(n) === 100 ? this.options.cursorWidth : 0}px)`, this.isScrollable && this.options.autoScroll && this.scrollIntoView(e, t);
  }
  exportImage(e, t, n) {
    return tr(this, void 0, void 0, function* () {
      const i = this.canvasWrapper.querySelectorAll("canvas");
      if (!i.length)
        throw new Error("No waveform data");
      if (n === "dataURL") {
        const o = Array.from(i).map((s) => s.toDataURL(e, t));
        return Promise.resolve(o);
      }
      return Promise.all(Array.from(i).map((o) => new Promise((s, a) => {
        o.toBlob((c) => {
          c ? s(c) : a(new Error("Could not export image"));
        }, e, t);
      })));
    });
  }
}
ke.MAX_CANVAS_WIDTH = 8e3;
ke.MAX_NODES = 10;
class Va extends Ge {
  constructor() {
    super(...arguments), this.unsubscribe = () => {
    };
  }
  start() {
    this.unsubscribe = this.on("tick", () => {
      requestAnimationFrame(() => {
        this.emit("tick");
      });
    }), this.emit("tick");
  }
  stop() {
    this.unsubscribe();
  }
  destroy() {
    this.unsubscribe();
  }
}
var zt = function(r, e, t, n) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(n.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(n.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((n = n.apply(r, e || [])).next());
  });
};
class Vt extends Ge {
  constructor(e = new AudioContext()) {
    super(), this.bufferNode = null, this.playStartTime = 0, this.playedDuration = 0, this._muted = !1, this._playbackRate = 1, this._duration = void 0, this.buffer = null, this.currentSrc = "", this.paused = !0, this.crossOrigin = null, this.seeking = !1, this.autoplay = !1, this.addEventListener = this.on, this.removeEventListener = this.un, this.audioContext = e, this.gainNode = this.audioContext.createGain(), this.gainNode.connect(this.audioContext.destination);
  }
  load() {
    return zt(this, void 0, void 0, function* () {
    });
  }
  get src() {
    return this.currentSrc;
  }
  set src(e) {
    if (this.currentSrc = e, this._duration = void 0, !e) {
      this.buffer = null, this.emit("emptied");
      return;
    }
    fetch(e).then((t) => {
      if (t.status >= 400)
        throw new Error(`Failed to fetch ${e}: ${t.status} (${t.statusText})`);
      return t.arrayBuffer();
    }).then((t) => this.currentSrc !== e ? null : this.audioContext.decodeAudioData(t)).then((t) => {
      this.currentSrc === e && (this.buffer = t, this.emit("loadedmetadata"), this.emit("canplay"), this.autoplay && this.play());
    });
  }
  _play() {
    var e;
    if (!this.paused) return;
    this.paused = !1, (e = this.bufferNode) === null || e === void 0 || e.disconnect(), this.bufferNode = this.audioContext.createBufferSource(), this.buffer && (this.bufferNode.buffer = this.buffer), this.bufferNode.playbackRate.value = this._playbackRate, this.bufferNode.connect(this.gainNode);
    let t = this.playedDuration * this._playbackRate;
    (t >= this.duration || t < 0) && (t = 0, this.playedDuration = 0), this.bufferNode.start(this.audioContext.currentTime, t), this.playStartTime = this.audioContext.currentTime, this.bufferNode.onended = () => {
      this.currentTime >= this.duration && (this.pause(), this.emit("ended"));
    };
  }
  _pause() {
    var e;
    this.paused = !0, (e = this.bufferNode) === null || e === void 0 || e.stop(), this.playedDuration += this.audioContext.currentTime - this.playStartTime;
  }
  play() {
    return zt(this, void 0, void 0, function* () {
      this.paused && (this._play(), this.emit("play"));
    });
  }
  pause() {
    this.paused || (this._pause(), this.emit("pause"));
  }
  stopAt(e) {
    const t = e - this.currentTime, n = this.bufferNode;
    n == null || n.stop(this.audioContext.currentTime + t), n == null || n.addEventListener("ended", () => {
      n === this.bufferNode && (this.bufferNode = null, this.pause());
    }, {
      once: !0
    });
  }
  setSinkId(e) {
    return zt(this, void 0, void 0, function* () {
      return this.audioContext.setSinkId(e);
    });
  }
  get playbackRate() {
    return this._playbackRate;
  }
  set playbackRate(e) {
    this._playbackRate = e, this.bufferNode && (this.bufferNode.playbackRate.value = e);
  }
  get currentTime() {
    return (this.paused ? this.playedDuration : this.playedDuration + (this.audioContext.currentTime - this.playStartTime)) * this._playbackRate;
  }
  set currentTime(e) {
    const t = !this.paused;
    t && this._pause(), this.playedDuration = e / this._playbackRate, t && this._play(), this.emit("seeking"), this.emit("timeupdate");
  }
  get duration() {
    var e, t;
    return (e = this._duration) !== null && e !== void 0 ? e : ((t = this.buffer) === null || t === void 0 ? void 0 : t.duration) || 0;
  }
  set duration(e) {
    this._duration = e;
  }
  get volume() {
    return this.gainNode.gain.value;
  }
  set volume(e) {
    this.gainNode.gain.value = e, this.emit("volumechange");
  }
  get muted() {
    return this._muted;
  }
  set muted(e) {
    this._muted !== e && (this._muted = e, this._muted ? this.gainNode.disconnect() : this.gainNode.connect(this.audioContext.destination));
  }
  canPlayType(e) {
    return /^(audio|video)\//.test(e);
  }
  /** Get the GainNode used to play the audio. Can be used to attach filters. */
  getGainNode() {
    return this.gainNode;
  }
  /** Get decoded audio */
  getChannelData() {
    const e = [];
    if (!this.buffer) return e;
    const t = this.buffer.numberOfChannels;
    for (let n = 0; n < t; n++)
      e.push(this.buffer.getChannelData(n));
    return e;
  }
}
var Me = function(r, e, t, n) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(n.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(n.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((n = n.apply(r, e || [])).next());
  });
};
const Ua = {
  waveColor: "#999",
  progressColor: "#555",
  cursorWidth: 1,
  minPxPerSec: 0,
  fillParent: !0,
  interact: !0,
  dragToSeek: !1,
  autoScroll: !0,
  autoCenter: !0,
  sampleRate: 8e3
};
class qe extends Ba {
  /** Create a new WaveSurfer instance */
  static create(e) {
    return new qe(e);
  }
  /** Create a new WaveSurfer instance */
  constructor(e) {
    const t = e.media || (e.backend === "WebAudio" ? new Vt() : void 0);
    super({
      media: t,
      mediaControls: e.mediaControls,
      autoplay: e.autoplay,
      playbackRate: e.audioRate
    }), this.plugins = [], this.decodedData = null, this.stopAtPosition = null, this.subscriptions = [], this.mediaSubscriptions = [], this.abortController = null, this.options = Object.assign({}, Ua, e), this.timer = new Va();
    const n = t ? void 0 : this.getMediaElement();
    this.renderer = new ke(this.options, n), this.initPlayerEvents(), this.initRendererEvents(), this.initTimerEvents(), this.initPlugins();
    const i = this.options.url || this.getSrc() || "";
    Promise.resolve().then(() => {
      this.emit("init");
      const {
        peaks: o,
        duration: s
      } = this.options;
      (i || o && s) && this.load(i, o, s).catch(() => null);
    });
  }
  updateProgress(e = this.getCurrentTime()) {
    return this.renderer.renderProgress(e / this.getDuration(), this.isPlaying()), e;
  }
  initTimerEvents() {
    this.subscriptions.push(this.timer.on("tick", () => {
      if (!this.isSeeking()) {
        const e = this.updateProgress();
        this.emit("timeupdate", e), this.emit("audioprocess", e), this.stopAtPosition != null && this.isPlaying() && e >= this.stopAtPosition && this.pause();
      }
    }));
  }
  initPlayerEvents() {
    this.isPlaying() && (this.emit("play"), this.timer.start()), this.mediaSubscriptions.push(this.onMediaEvent("timeupdate", () => {
      const e = this.updateProgress();
      this.emit("timeupdate", e);
    }), this.onMediaEvent("play", () => {
      this.emit("play"), this.timer.start();
    }), this.onMediaEvent("pause", () => {
      this.emit("pause"), this.timer.stop(), this.stopAtPosition = null;
    }), this.onMediaEvent("emptied", () => {
      this.timer.stop(), this.stopAtPosition = null;
    }), this.onMediaEvent("ended", () => {
      this.emit("timeupdate", this.getDuration()), this.emit("finish"), this.stopAtPosition = null;
    }), this.onMediaEvent("seeking", () => {
      this.emit("seeking", this.getCurrentTime());
    }), this.onMediaEvent("error", () => {
      var e;
      this.emit("error", (e = this.getMediaElement().error) !== null && e !== void 0 ? e : new Error("Media error")), this.stopAtPosition = null;
    }));
  }
  initRendererEvents() {
    this.subscriptions.push(
      // Seek on click
      this.renderer.on("click", (e, t) => {
        this.options.interact && (this.seekTo(e), this.emit("interaction", e * this.getDuration()), this.emit("click", e, t));
      }),
      // Double click
      this.renderer.on("dblclick", (e, t) => {
        this.emit("dblclick", e, t);
      }),
      // Scroll
      this.renderer.on("scroll", (e, t, n, i) => {
        const o = this.getDuration();
        this.emit("scroll", e * o, t * o, n, i);
      }),
      // Redraw
      this.renderer.on("render", () => {
        this.emit("redraw");
      }),
      // RedrawComplete
      this.renderer.on("rendered", () => {
        this.emit("redrawcomplete");
      }),
      // DragStart
      this.renderer.on("dragstart", (e) => {
        this.emit("dragstart", e);
      }),
      // DragEnd
      this.renderer.on("dragend", (e) => {
        this.emit("dragend", e);
      })
    );
    {
      let e;
      this.subscriptions.push(this.renderer.on("drag", (t) => {
        if (!this.options.interact) return;
        this.renderer.renderProgress(t), clearTimeout(e);
        let n;
        this.isPlaying() ? n = 0 : this.options.dragToSeek === !0 ? n = 200 : typeof this.options.dragToSeek == "object" && this.options.dragToSeek !== void 0 && (n = this.options.dragToSeek.debounceTime), e = setTimeout(() => {
          this.seekTo(t);
        }, n), this.emit("interaction", t * this.getDuration()), this.emit("drag", t);
      }));
    }
  }
  initPlugins() {
    var e;
    !((e = this.options.plugins) === null || e === void 0) && e.length && this.options.plugins.forEach((t) => {
      this.registerPlugin(t);
    });
  }
  unsubscribePlayerEvents() {
    this.mediaSubscriptions.forEach((e) => e()), this.mediaSubscriptions = [];
  }
  /** Set new wavesurfer options and re-render it */
  setOptions(e) {
    this.options = Object.assign({}, this.options, e), e.duration && !e.peaks && (this.decodedData = it.createBuffer(this.exportPeaks(), e.duration)), e.peaks && e.duration && (this.decodedData = it.createBuffer(e.peaks, e.duration)), this.renderer.setOptions(this.options), e.audioRate && this.setPlaybackRate(e.audioRate), e.mediaControls != null && (this.getMediaElement().controls = e.mediaControls);
  }
  /** Register a wavesurfer.js plugin */
  registerPlugin(e) {
    return e._init(this), this.plugins.push(e), this.subscriptions.push(e.once("destroy", () => {
      this.plugins = this.plugins.filter((t) => t !== e);
    })), e;
  }
  /** For plugins only: get the waveform wrapper div */
  getWrapper() {
    return this.renderer.getWrapper();
  }
  /** For plugins only: get the scroll container client width */
  getWidth() {
    return this.renderer.getWidth();
  }
  /** Get the current scroll position in pixels */
  getScroll() {
    return this.renderer.getScroll();
  }
  /** Set the current scroll position in pixels */
  setScroll(e) {
    return this.renderer.setScroll(e);
  }
  /** Move the start of the viewing window to a specific time in the audio (in seconds) */
  setScrollTime(e) {
    const t = e / this.getDuration();
    this.renderer.setScrollPercentage(t);
  }
  /** Get all registered plugins */
  getActivePlugins() {
    return this.plugins;
  }
  loadAudio(e, t, n, i) {
    return Me(this, void 0, void 0, function* () {
      var o;
      if (this.emit("load", e), !this.options.media && this.isPlaying() && this.pause(), this.decodedData = null, this.stopAtPosition = null, !t && !n) {
        const a = this.options.fetchParams || {};
        window.AbortController && !a.signal && (this.abortController = new AbortController(), a.signal = (o = this.abortController) === null || o === void 0 ? void 0 : o.signal);
        const c = (u) => this.emit("loading", u);
        t = yield Wa.fetchBlob(e, c, a);
        const l = this.options.blobMimeType;
        l && (t = new Blob([t], {
          type: l
        }));
      }
      this.setSrc(e, t);
      const s = yield new Promise((a) => {
        const c = i || this.getDuration();
        c ? a(c) : this.mediaSubscriptions.push(this.onMediaEvent("loadedmetadata", () => a(this.getDuration()), {
          once: !0
        }));
      });
      if (!e && !t) {
        const a = this.getMediaElement();
        a instanceof Vt && (a.duration = s);
      }
      if (n)
        this.decodedData = it.createBuffer(n, s || 0);
      else if (t) {
        const a = yield t.arrayBuffer();
        this.decodedData = yield it.decode(a, this.options.sampleRate);
      }
      this.decodedData && (this.emit("decode", this.getDuration()), this.renderer.render(this.decodedData)), this.emit("ready", this.getDuration());
    });
  }
  /** Load an audio file by URL, with optional pre-decoded audio data */
  load(e, t, n) {
    return Me(this, void 0, void 0, function* () {
      try {
        return yield this.loadAudio(e, void 0, t, n);
      } catch (i) {
        throw this.emit("error", i), i;
      }
    });
  }
  /** Load an audio blob */
  loadBlob(e, t, n) {
    return Me(this, void 0, void 0, function* () {
      try {
        return yield this.loadAudio("", e, t, n);
      } catch (i) {
        throw this.emit("error", i), i;
      }
    });
  }
  /** Zoom the waveform by a given pixels-per-second factor */
  zoom(e) {
    if (!this.decodedData)
      throw new Error("No audio loaded");
    this.renderer.zoom(e), this.emit("zoom", e);
  }
  /** Get the decoded audio data */
  getDecodedData() {
    return this.decodedData;
  }
  /** Get decoded peaks */
  exportPeaks({
    channels: e = 2,
    maxLength: t = 8e3,
    precision: n = 1e4
  } = {}) {
    if (!this.decodedData)
      throw new Error("The audio has not been decoded yet");
    const i = Math.min(e, this.decodedData.numberOfChannels), o = [];
    for (let s = 0; s < i; s++) {
      const a = this.decodedData.getChannelData(s), c = [], l = a.length / t;
      for (let u = 0; u < t; u++) {
        const d = a.slice(Math.floor(u * l), Math.ceil((u + 1) * l));
        let h = 0;
        for (let p = 0; p < d.length; p++) {
          const b = d[p];
          Math.abs(b) > Math.abs(h) && (h = b);
        }
        c.push(Math.round(h * n) / n);
      }
      o.push(c);
    }
    return o;
  }
  /** Get the duration of the audio in seconds */
  getDuration() {
    let e = super.getDuration() || 0;
    return (e === 0 || e === 1 / 0) && this.decodedData && (e = this.decodedData.duration), e;
  }
  /** Toggle if the waveform should react to clicks */
  toggleInteraction(e) {
    this.options.interact = e;
  }
  /** Jump to a specific time in the audio (in seconds) */
  setTime(e) {
    this.stopAtPosition = null, super.setTime(e), this.updateProgress(e), this.emit("timeupdate", e);
  }
  /** Seek to a percentage of audio as [0..1] (0 = beginning, 1 = end) */
  seekTo(e) {
    const t = this.getDuration() * e;
    this.setTime(t);
  }
  /** Start playing the audio */
  play(e, t) {
    const n = Object.create(null, {
      play: {
        get: () => super.play
      }
    });
    return Me(this, void 0, void 0, function* () {
      e != null && this.setTime(e);
      const i = yield n.play.call(this);
      return t != null && (this.media instanceof Vt ? this.media.stopAt(t) : this.stopAtPosition = t), i;
    });
  }
  /** Play or pause the audio */
  playPause() {
    return Me(this, void 0, void 0, function* () {
      return this.isPlaying() ? this.pause() : this.play();
    });
  }
  /** Stop the audio and go to the beginning */
  stop() {
    this.pause(), this.setTime(0);
  }
  /** Skip N or -N seconds from the current position */
  skip(e) {
    this.setTime(this.getCurrentTime() + e);
  }
  /** Empty the waveform */
  empty() {
    this.load("", [[0]], 1e-3);
  }
  /** Set HTML media element */
  setMediaElement(e) {
    this.unsubscribePlayerEvents(), super.setMediaElement(e), this.initPlayerEvents();
  }
  exportImage() {
    return Me(this, arguments, void 0, function* (e = "image/png", t = 1, n = "dataURL") {
      return this.renderer.exportImage(e, t, n);
    });
  }
  /** Unmount wavesurfer */
  destroy() {
    var e;
    this.emit("destroy"), (e = this.abortController) === null || e === void 0 || e.abort(), this.plugins.forEach((t) => t.destroy()), this.subscriptions.forEach((t) => t()), this.unsubscribePlayerEvents(), this.timer.destroy(), this.renderer.destroy(), super.destroy();
  }
}
qe.BasePlugin = Oa;
qe.dom = Da;
function Xa({
  container: r,
  onStop: e
}) {
  const t = me(null), [n, i] = $e(!1), o = ct(() => {
    var c;
    (c = t.current) == null || c.startRecording();
  }), s = ct(() => {
    var c;
    (c = t.current) == null || c.stopRecording();
  }), a = ct(e);
  return Ee(() => {
    if (r) {
      const l = qe.create({
        normalize: !1,
        container: r
      }).registerPlugin(fn.create());
      t.current = l, l.on("record-start", () => {
        i(!0);
      }), l.on("record-end", (u) => {
        a(u), i(!1);
      });
    }
  }, [r, a]), {
    recording: n,
    start: o,
    stop: s
  };
}
function Ga(r) {
  const e = function(a, c, l) {
    for (let u = 0; u < l.length; u++)
      a.setUint8(c + u, l.charCodeAt(u));
  }, t = r.numberOfChannels, n = r.length * t * 2 + 44, i = new ArrayBuffer(n), o = new DataView(i);
  let s = 0;
  e(o, s, "RIFF"), s += 4, o.setUint32(s, n - 8, !0), s += 4, e(o, s, "WAVE"), s += 4, e(o, s, "fmt "), s += 4, o.setUint32(s, 16, !0), s += 4, o.setUint16(s, 1, !0), s += 2, o.setUint16(s, t, !0), s += 2, o.setUint32(s, r.sampleRate, !0), s += 4, o.setUint32(s, r.sampleRate * 2 * t, !0), s += 4, o.setUint16(s, t * 2, !0), s += 2, o.setUint16(s, 16, !0), s += 2, e(o, s, "data"), s += 4, o.setUint32(s, r.length * t * 2, !0), s += 4;
  for (let a = 0; a < r.numberOfChannels; a++) {
    const c = r.getChannelData(a);
    for (let l = 0; l < c.length; l++)
      o.setInt16(s, c[l] * 65535, !0), s += 2;
  }
  return new Uint8Array(i);
}
async function qa(r, e, t) {
  const n = await r.arrayBuffer(), o = await new AudioContext().decodeAudioData(n), s = new AudioContext(), a = o.numberOfChannels, c = o.sampleRate;
  let l = o.length, u = 0;
  const d = s.createBuffer(a, l, c);
  for (let h = 0; h < a; h++) {
    const p = o.getChannelData(h), b = d.getChannelData(h);
    for (let v = 0; v < l; v++)
      b[v] = p[u + v];
  }
  return Promise.resolve(Ga(d));
}
const Ka = (r) => !!r.name, He = (r) => {
  var e;
  return {
    text: (r == null ? void 0 : r.text) || "",
    files: ((e = r == null ? void 0 : r.files) == null ? void 0 : e.map((t) => t.path)) || []
  };
}, Qa = So(({
  onValueChange: r,
  onChange: e,
  onPasteFile: t,
  onUpload: n,
  onSubmit: i,
  onRemove: o,
  onDownload: s,
  onDrop: a,
  onPreview: c,
  upload: l,
  onCancel: u,
  children: d,
  readOnly: h,
  loading: p,
  disabled: b,
  placeholder: v,
  elRef: g,
  slots: m,
  // setSlotParams,
  uploadConfig: x,
  value: E,
  ...y
}) => {
  var we, xe;
  const [_, w] = $e(!1), T = si(), C = me(null), [P, M] = $e(!1), D = Jn(y.actions, !0), N = Jn(y.footer, !0), {
    token: F
  } = ze.useToken(), {
    start: W,
    stop: L,
    recording: H
  } = Xa({
    container: C.current,
    async onStop(U) {
      const A = new File([await qa(U)], `${Date.now()}_recording_result.wav`, {
        type: "audio/wav"
      });
      te(A);
    }
  }), [O, z] = Ra({
    onValueChange: r,
    value: E
  }), S = Ut(() => ri(x), [x]), se = b || (S == null ? void 0 : S.disabled) || p || h || P, te = ct(async (U) => {
    try {
      if (se)
        return;
      M(!0);
      const A = S == null ? void 0 : S.maxCount;
      if (typeof A == "number" && A > 0 && j.length >= A)
        return;
      let B = Array.isArray(U) ? U : [U];
      if (A === 1)
        B = B.slice(0, 1);
      else if (B.length === 0) {
        M(!1);
        return;
      } else if (typeof A == "number") {
        const G = A - j.length;
        B = B.slice(0, G < 0 ? 0 : G);
      }
      const de = j, K = B.map((G) => ({
        ...G,
        size: G.size,
        uid: `${G.name}-${Date.now()}`,
        name: G.name,
        status: "uploading"
      }));
      Z((G) => [...A === 1 ? [] : G, ...K]);
      const J = (await l(B)).filter(Boolean).map((G, pe) => ({
        ...G,
        uid: K[pe].uid
      })), le = A === 1 ? J : [...de, ...J];
      n == null || n(J.map((G) => G.path)), M(!1);
      const fe = {
        ...O,
        files: le
      };
      return e == null || e(He(fe)), z(fe), J;
    } catch {
      return M(!1), [];
    }
  }), [j, Z] = $e(() => (O == null ? void 0 : O.files) || []);
  Ee(() => {
    Z((O == null ? void 0 : O.files) || []);
  }, [O == null ? void 0 : O.files]);
  const X = Ut(() => {
    const U = {};
    return j.map((A) => {
      if (!Ka(A)) {
        const B = A.uid || A.url || A.path;
        return U[B] || (U[B] = 0), U[B]++, {
          ...A,
          name: A.orig_name || A.path,
          uid: A.uid || B + "-" + U[B],
          status: "done"
        };
      }
      return A;
    }) || [];
  }, [j]), Q = (S == null ? void 0 : S.allowUpload) ?? !0, ae = Q ? S == null ? void 0 : S.allowSpeech : !1, he = Q ? S == null ? void 0 : S.allowPasteFile : !1;
  return /* @__PURE__ */ re.jsxs(re.Fragment, {
    children: [/* @__PURE__ */ re.jsx("div", {
      style: {
        display: "none"
      },
      ref: C
    }), /* @__PURE__ */ re.jsx("div", {
      style: {
        display: "none"
      },
      children: d
    }), /* @__PURE__ */ re.jsx(sn, {
      ...y,
      value: O == null ? void 0 : O.text,
      ref: g,
      disabled: b,
      readOnly: h,
      allowSpeech: ae ? {
        recording: H,
        onRecordingChange(U) {
          se || (U ? W() : L());
        }
      } : !1,
      placeholder: v,
      loading: p,
      onSubmit: () => {
        T || i == null || i(He(O));
      },
      onCancel: () => {
        u == null || u();
      },
      onChange: (U) => {
        const A = {
          ...O,
          text: U
        };
        e == null || e(He(A)), z(A);
      },
      onPasteFile: async (U, A) => {
        if (!(he ?? !0))
          return;
        const B = await te(Array.from(A));
        B && (t == null || t(B.map((de) => de.path)));
      },
      prefix: /* @__PURE__ */ re.jsxs(re.Fragment, {
        children: [Q ? /* @__PURE__ */ re.jsx(Li, {
          title: S == null ? void 0 : S.uploadButtonTooltip,
          children: /* @__PURE__ */ re.jsx(Oi, {
            count: ((S == null ? void 0 : S.showCount) ?? !0) && !_ ? X.length : 0,
            children: /* @__PURE__ */ re.jsx(Ie, {
              onClick: () => {
                w(!_);
              },
              color: "default",
              variant: "text",
              icon: /* @__PURE__ */ re.jsx(_i, {})
            })
          })
        }) : null, m.prefix ? /* @__PURE__ */ re.jsx(Ke, {
          slot: m.prefix
        }) : null]
      }),
      actions: m.actions ? /* @__PURE__ */ re.jsx(Ke, {
        slot: m.actions
      }) : D || y.actions,
      footer: m.footer ? /* @__PURE__ */ re.jsx(Ke, {
        slot: m.footer
      }) : N || y.footer,
      header: Q ? /* @__PURE__ */ re.jsx(sn.Header, {
        title: (S == null ? void 0 : S.title) || "Attachments",
        open: _,
        onOpenChange: w,
        children: /* @__PURE__ */ re.jsx(Fr, {
          ...Ta(ii(S, ["title", "placeholder", "showCount", "buttonTooltip", "allowPasteFile"])),
          imageProps: {
            ...S == null ? void 0 : S.imageProps,
            wrapperStyle: {
              width: "100%",
              height: "100%",
              ...(we = S == null ? void 0 : S.imageProps) == null ? void 0 : we.wrapperStyle
            },
            style: {
              width: "100%",
              height: "100%",
              objectFit: "contain",
              borderRadius: F.borderRadius,
              ...(xe = S == null ? void 0 : S.imageProps) == null ? void 0 : xe.style
            }
          },
          disabled: se,
          getDropContainer: () => S != null && S.fullscreenDrop ? document.body : null,
          items: X,
          placeholder: (U) => {
            var B, de, K, J, le, fe, G, pe, be, I, Y, ne;
            const A = U === "drop";
            return {
              title: A ? ((de = (B = S == null ? void 0 : S.placeholder) == null ? void 0 : B.drop) == null ? void 0 : de.title) ?? "Drop file here" : ((J = (K = S == null ? void 0 : S.placeholder) == null ? void 0 : K.inline) == null ? void 0 : J.title) ?? "Upload files",
              description: A ? ((fe = (le = S == null ? void 0 : S.placeholder) == null ? void 0 : le.drop) == null ? void 0 : fe.description) ?? void 0 : ((pe = (G = S == null ? void 0 : S.placeholder) == null ? void 0 : G.inline) == null ? void 0 : pe.description) ?? "Click or drag files to this area to upload",
              icon: A ? ((I = (be = S == null ? void 0 : S.placeholder) == null ? void 0 : be.drop) == null ? void 0 : I.icon) ?? void 0 : ((ne = (Y = S == null ? void 0 : S.placeholder) == null ? void 0 : Y.inline) == null ? void 0 : ne.icon) ?? /* @__PURE__ */ re.jsx(Ei, {})
            };
          },
          onDownload: s,
          onPreview: c,
          onDrop: a,
          onChange: async (U) => {
            try {
              const A = U.file, B = U.fileList, de = X.findIndex((K) => K.uid === A.uid);
              if (de !== -1) {
                if (se)
                  return;
                o == null || o(A);
                const K = j.slice();
                K.splice(de, 1);
                const J = {
                  ...O,
                  files: K
                };
                z(J), e == null || e(He(J));
              } else {
                if (se)
                  return;
                M(!0);
                let K = B.filter((I) => I.status !== "done");
                const J = S == null ? void 0 : S.maxCount;
                if (J === 1)
                  K = K.slice(0, 1);
                else if (K.length === 0) {
                  M(!1);
                  return;
                } else if (typeof J == "number") {
                  const I = J - j.length;
                  K = K.slice(0, I < 0 ? 0 : I);
                }
                const le = j, fe = K.map((I) => ({
                  ...I,
                  size: I.size,
                  uid: I.uid,
                  name: I.name,
                  status: "uploading"
                }));
                Z((I) => [...J === 1 ? [] : I, ...fe]);
                const G = (await l(K.map((I) => I.originFileObj))).filter(Boolean).map((I, Y) => ({
                  ...I,
                  uid: fe[Y].uid
                })), pe = J === 1 ? G : [...le, ...G];
                n == null || n(G.map((I) => I.path)), M(!1);
                const be = {
                  ...O,
                  files: pe
                };
                Z(pe), r == null || r(be), e == null || e(He(be));
              }
            } catch (A) {
              M(!1), console.error(A);
            }
          },
          customRequest: zi
        })
      }) : m.header ? /* @__PURE__ */ re.jsx(Ke, {
        slot: m.header
      }) : y.header
    })]
  });
});
export {
  Qa as MultimodalInput,
  Qa as default
};
