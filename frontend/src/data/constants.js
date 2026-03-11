// frontend/src/data/constants.js

// [통합] 자연계열 표준 모집 단위 (모든 대학 공통 사용)
export const UNIVERSAL_NATURAL_CLUSTERS = [
  {
    value: "HIGH_TECH",
    label: "💻 IT/SW/컴퓨터/인공지능 (최상위 경쟁)",
    weight_modifier: 1.08 // 컷라인 보정용 (옵션)
  },
  {
    value: "MAJOR_ENG",
    label: "⚙️ 주요 공학 (전자/전기/기계/화공/신소재)",
    weight_modifier: 1.03
  },
  {
    value: "PURE_SCI",
    label: "🧪 자연과학/바이오/건축/산공",
    weight_modifier: 0.98
  },
  {
    value: "ETC_NAT",
    label: "📐 기타 이공계열",
    weight_modifier: 0.95
  }
];

// [통합] 인문계열 표준 모집 단위
export const UNIVERSAL_HUMAN_CLUSTERS = [
  { value: "BIZ_TOP", label: "📈 경영/경제/통계/미디어 (최상위 경쟁)" },
  { value: "SOC_SCI", label: "⚖️ 사회과학/행정/정치/심리" },
  { value: "HUM_LIT", label: "📚 인문/어문/철학/사학" },
  { value: "ETC_HUM", label: "🎓 기타 인문계열" }
];