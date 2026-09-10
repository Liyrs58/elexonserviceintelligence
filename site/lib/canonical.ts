export const nav = [
  { href: '/', label: 'Overview' },
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/findings', label: 'Findings' },
  { href: '/methodology', label: 'Methodology' },
  { href: '/interview', label: 'Candidate view' },
  { href: '/downloads', label: 'Downloads' },
];

export const metrics = [
  { value: '4,418', label: 'validated periods', detail: '4,418 expected' },
  { value: '130', label: 'review flags', detail: 'not incident counts' },
  { value: '100%', label: 'core completeness', detail: '0 validation exceptions' },
  { value: '38', label: 'passing tests', detail: 'reproducible controls' },
];

export const dashboardPages = [
  { slug: 'monitor', title: 'Settlement Service Monitor', decision: 'What does this historical snapshot show, and which periods require review?', image: '/dashboard/monitor.png' },
  { slug: 'analysis', title: 'Market & Settlement Analysis', decision: 'How do distributions, system length and NIV/price association differ?', image: '/dashboard/analysis.png' },
  { slug: 'investigation', title: 'Exception Investigation', decision: 'What happened, what is known, and what evidence should be checked next?', image: '/dashboard/investigation.png' },
  { slug: 'controls', title: 'Data Quality & Controls', decision: 'Can the selected snapshot be trusted, including the clock-change day?', image: '/dashboard/controls.png' },
];

export const workflow = ['Control', 'Detect', 'Investigate', 'Communicate', 'Recommend'];
