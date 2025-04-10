module.exports = {
    content: [
        './static/**/*.html',
    ],
    theme: {
        extend: {
            colors: {
                primary: '#6b46c1',  // 主要紫色
                secondary: '#553c9a', // 更深的紫色
                accent: '#f6ad55',    // 温暖的橙色
                text: '#2d3748',      // 文本颜色
                'light-color': '#f8f9fa',
                'light-gray': '#edf2f7',
                'dark-color': '#1a202c',
                success: '#48bb78',
            },
            boxShadow: {
                'sm': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
                'md': '0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)',
                'lg': '0 10px 25px rgba(0, 0, 0, 0.1), 0 5px 10px rgba(0, 0, 0, 0.05)',
            },
            borderRadius: {
                DEFAULT: '10px',
            },
            transitionProperty: {
                'DEFAULT': 'all',
            },
            transitionTimingFunction: {
                'DEFAULT': 'cubic-bezier(0.25, 0.8, 0.25, 1)',
            },
            transitionDuration: {
                'DEFAULT': '300ms',
            }
        },
    },
    plugins: [],
}
