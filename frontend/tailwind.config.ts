import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}', // For 'pages' dir if it exists
    './app/**/*.{js,ts,jsx,tsx,mdx}',     // Scans the 'app' dir
    './components/**/*.{js,ts,jsx,tsx,mdx}', // Scans our 'components' dir
  ],
  theme: {
    extend: {
      // You can add custom theme settings here later
    },
  },
  plugins: [],
};
export default config;