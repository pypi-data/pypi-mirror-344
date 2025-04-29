from setuptools import setup, find_packages

setup(
    name='multi_desktop_monitor',
    version='0.1',
    packages=find_packages(),  # Automatically finds the package directories
    install_requires=[
        'watchdog',
        'requests',
        'scapy',
        'Flask',
        'dash',
        'dash-bootstrap-components',
        'pandas',
        'plotly'
    ],
    entry_points={
        'console_scripts': [
            'start_agent=multiple_desktop_monitor.agent.agent:main',  # Entry point for agent
            'start_dashboard=multiple_desktop_monitor.dashboard.dashboard:main'  # Entry point for dashboard
        ],
    },
)
