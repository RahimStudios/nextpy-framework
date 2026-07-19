/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Framework templates and components
    "./pages/**/*.{py,jsx,html}",
    "./components/**/*.{py,jsx,html}",
    "./templates/**/*.{html,htm}",
    "./public/**/*.html",

    // Also scan from project root (two level up)
    "../../templates/**/*.{html,htm}",
    "../../pages/**/*.{py,jsx,html}",
    "../../components/**/*.{py,jsx,html}",
  ],
  // Force include common Tailwind classes
  safelist: [
    // Background colors
    'bg-blue-50', 'bg-blue-100', 'bg-blue-200', 'bg-blue-300', 'bg-blue-400', 'bg-blue-500', 'bg-blue-600', 'bg-blue-700',
    'bg-red-50', 'bg-red-100', 'bg-red-200', 'bg-red-300', 'bg-red-400', 'bg-red-500', 'bg-red-600', 'bg-red-700',
    'bg-green-50', 'bg-green-100', 'bg-green-200', 'bg-green-300', 'bg-green-400', 'bg-green-500', 'bg-green-600', 'bg-green-700',
    'bg-purple-50', 'bg-purple-100', 'bg-purple-200', 'bg-purple-300', 'bg-purple-400', 'bg-purple-500', 'bg-purple-600', 'bg-purple-700',
    'bg-gray-50', 'bg-gray-100', 'bg-gray-200', 'bg-gray-300', 'bg-gray-400', 'bg-gray-500', 'bg-gray-600', 'bg-gray-700', 'bg-gray-800', 'bg-gray-900',
    'bg-white', 'bg-black',

    // Text colors
    'text-blue-50', 'text-blue-100', 'text-blue-200', 'text-blue-300', 'text-blue-400', 'text-blue-500', 'text-blue-600', 'text-blue-700',
    'text-red-50', 'text-red-100', 'text-red-200', 'text-red-300', 'text-red-400', 'text-red-500', 'text-red-600', 'text-red-700',
    'text-green-50', 'text-green-100', 'text-green-200', 'text-green-300', 'text-green-400', 'text-green-500', 'text-green-600', 'text-green-700',
    'text-purple-50', 'text-purple-100', 'text-purple-200', 'text-purple-300', 'text-purple-400', 'text-purple-500', 'text-purple-600', 'text-purple-700',
    'text-gray-50', 'text-gray-100', 'text-gray-200', 'text-gray-300', 'text-gray-400', 'text-gray-500', 'text-gray-600', 'text-gray-700', 'text-gray-800', 'text-gray-900',
    'text-white', 'text-black',

    // Shadows
    'shadow-sm', 'shadow', 'shadow-md', 'shadow-lg', 'shadow-xl', 'shadow-2xl',

    // Gradients
    'bg-gradient-to-r', 'bg-gradient-to-br', 'bg-gradient-to-b', 'bg-gradient-to-bl', 'bg-gradient-to-l', 'bg-gradient-to-tl', 'bg-gradient-to-t', 'bg-gradient-to-tr',
    'from-blue-50', 'from-blue-100', 'from-blue-200', 'from-blue-300', 'from-blue-400', 'from-blue-500', 'from-blue-600', 'from-blue-700',
    'via-indigo-50', 'via-indigo-100', 'via-indigo-200', 'via-indigo-300', 'via-indigo-400', 'via-indigo-500', 'via-indigo-600', 'via-indigo-700',
    'to-purple-50', 'to-purple-100', 'to-purple-200', 'to-purple-300', 'to-purple-400', 'to-purple-500', 'to-purple-600', 'to-purple-700',

    // Spacing and layout
    'p-4', 'p-6', 'p-8', 'px-4', 'px-6', 'px-8', 'py-2', 'py-4', 'py-6', 'py-8', 'py-12', 'py-16', 'py-20', 'py-24',
    'm-4', 'm-6', 'm-8', 'mx-4', 'mx-6', 'mx-8', 'my-2', 'my-4', 'my-6', 'my-8', 'my-12', 'my-16', 'my-20', 'my-24',
    'mb-2', 'mb-4', 'mb-6', 'mb-8', 'mb-12', 'mb-16', 'mb-20', 'mb-24',
    'mt-2', 'mt-4', 'mt-6', 'mt-8', 'mt-12', 'mt-16', 'mt-20', 'mt-24',

    // Borders and rounded
    'border', 'border-2', 'border-l-4', 'border-t-4', 'rounded', 'rounded-lg', 'rounded-xl', 'rounded-full',

    // Flexbox and grid
    'flex', 'flex-col', 'flex-row', 'items-center', 'justify-center', 'justify-between', 'grid', 'grid-cols-2', 'grid-cols-3', 'grid-cols-4', 'gap-4', 'gap-6', 'gap-8',

    // Width and height
    'w-full', 'w-1/2', 'w-1/3', 'w-1/4', 'h-full', 'h-screen', 'max-w-md', 'max-w-lg', 'max-w-xl', 'max-w-4xl', 'max-w-6xl', 'max-w-7xl',

    // Typography
    'text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl', 'text-3xl', 'text-4xl', 'text-5xl', 'text-6xl', 'text-7xl',
    'font-light', 'font-normal', 'font-medium', 'font-semibold', 'font-bold',
    'leading-tight', 'leading-relaxed', 'leading-loose',
    'text-center', 'text-left', 'text-right',

    // Hover states
    'hover:bg-blue-600', 'hover:bg-blue-700', 'hover:bg-purple-600', 'hover:bg-purple-700', 'hover:bg-green-600', 'hover:bg-green-700',
    'hover:text-white', 'hover:text-blue-600', 'hover:text-purple-600', 'hover:text-green-600',
    'hover:shadow-lg', 'hover:shadow-xl', 'hover:scale-105', 'hover:translate-x-1',

    // Transitions
    'transition', 'transition-all', 'transition-colors', 'transition-transform',

    // Opacity and visibility
    'opacity-0', 'opacity-50', 'opacity-100', 'invisible', 'visible',

    // Z-index
    'z-10', 'z-20', 'z-30', 'z-40', 'z-50',

    // Positioning
    'relative', 'absolute', 'fixed', 'sticky', 'top-0', 'bottom-0', 'left-0', 'right-0'
  ],
  plugins: [],
};