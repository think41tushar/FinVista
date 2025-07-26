import { Link } from 'react-router-dom';

export default function LandingPage() {
  return (
    <section className="relative isolate overflow-hidden text-white min-h-screen" style={{ backgroundColor: 'var(--color-bg-primary)' }}>
      {/* Light Grid Texture */}
      <div className="pointer-events-none absolute inset-0 bg-[url('/grid.svg')] bg-repeat opacity-10" />
      
      {/* Aurora Accent */}
      <div className="pointer-events-none absolute left-1/2 top-1/2 -z-10 h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full blur-3xl" style={{ backgroundColor: 'rgba(27, 156, 133, 0.15)' }} />
      
      {/* Main container */}
      <div className="relative mx-auto flex max-w-7xl flex-col items-center px-6 py-24 sm:py-28 lg:flex-row lg:justify-between lg:gap-8 lg:py-32">
        <div className="flex flex-col lg:max-w-xl">
          {/* Headline */}
          <h1 className="mb-6 max-w-xl text-center font-sans text-4xl font-semibold leading-tight sm:text-5xl lg:mb-8 lg:text-left">
            See the <span style={{ color: 'var(--color-accent)' }}>full picture</span> of your finances in one glance with <span style={{ color: 'var(--color-accent)' }}>FinVista</span>
          </h1>
          
          {/* Sub-headline */}
          <p className="mb-10 max-w-md text-center text-lg/relaxed text-slate-200 lg:mb-12 lg:text-left">
            Consolidate accounts, decode spending patterns, and unlock AI-powered insights designed to boost returns—securely, instantly, effortlessly.
          </p>
          
          {/* Calls to action */}
          <div className="flex gap-4 justify-center lg:justify-start">
            <Link to="/login" className="inline-flex items-center justify-center rounded-md px-6 py-3 font-medium shadow transition-colors" style={{ backgroundColor: 'var(--color-accent)', color: 'var(--color-white)' }} onMouseEnter={(e) => e.target.style.backgroundColor = 'var(--color-accent-light)'} onMouseLeave={(e) => e.target.style.backgroundColor = 'var(--color-accent)'}>
              Try FinVista free
            </Link>
            <a href="#feature-tour" className="inline-flex items-center justify-center rounded-md border border-slate-500 px-6 py-3 font-medium text-slate-200 hover:bg-white/10">
              Product tour
            </a>
          </div>
        </div>
        
        {/* App Preview/Illustration */}
        <div className="hidden lg:block lg:w-1/2">
          <div className="rounded-xl overflow-hidden shadow-2xl border border-slate-700/50 backdrop-blur-sm bg-white/5">
            <div className="p-4 border-b border-slate-700/50 flex items-center">
              <div className="flex space-x-2">
                <div className="w-3 h-3 rounded-full bg-red-400"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                <div className="w-3 h-3 rounded-full bg-green-400"></div>
              </div>
              <div className="text-xs text-slate-300 mx-auto">FinVista Dashboard</div>
            </div>
            <div className="p-4">
              <img 
                src="https://i.ibb.co/1f5ms6F0/A-highly-detailed-3-D-render-of-a-Fin-Vista-app-icon-for-a-website-styled-as-a-cinematic-3-D-model-w.jpg" 
                alt="FinVista Dashboard Preview" 
                className="w-full h-auto rounded-lg" 
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = '/fallback-dashboard.png';
                }}
              />
            </div>
          </div>
        </div>
      </div>
      
      {/* Features section */}
      <div id="feature-tour" className="relative mx-auto max-w-7xl px-6 py-16">
        <h2 className="text-center text-3xl font-semibold mb-16">
          Powerful <span style={{ color: 'var(--color-accent)' }}>financial tools</span> at your fingertips
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="p-6 rounded-xl bg-white/5 backdrop-blur-sm border border-slate-700/50">
            <div className="w-12 h-12 rounded-full flex items-center justify-center mb-4" style={{ backgroundColor: 'rgba(27, 156, 133, 0.2)' }}>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" style={{ color: 'var(--color-accent)' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-xl font-medium mb-2">AI-Powered Analytics</h3>
            <p className="text-slate-300">Advanced algorithms analyze your spending patterns to provide personalized insights and recommendations.</p>
          </div>
          
          {/* Feature 2 */}
          <div className="p-6 rounded-xl bg-white/5 backdrop-blur-sm border border-slate-700/50">
            <div className="w-12 h-12 rounded-full flex items-center justify-center mb-4" style={{ backgroundColor: 'rgba(27, 156, 133, 0.2)' }}>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" style={{ color: 'var(--color-accent)' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="text-xl font-medium mb-2">Bank-Level Security</h3>
            <p className="text-slate-300">Your financial data is protected with industry-leading encryption and security protocols.</p>
          </div>
          
          {/* Feature 3 */}
          <div className="p-6 rounded-xl bg-white/5 backdrop-blur-sm border border-slate-700/50">
            <div className="w-12 h-12 rounded-full flex items-center justify-center mb-4" style={{ backgroundColor: 'rgba(27, 156, 133, 0.2)' }}>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" style={{ color: 'var(--color-accent)' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-medium mb-2">Smart Budgeting</h3>
            <p className="text-slate-300">Create and track budgets that adapt to your spending habits and financial goals.</p>
          </div>
        </div>
      </div>
      
      {/* Footer */}
      <footer className="border-t border-slate-700/50 py-8">
        <div className="mx-auto max-w-7xl px-6 flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <h2 className="font-bold text-xl">FinVista</h2>
            <p className="text-sm text-slate-400">© 2025 All rights reserved</p>
          </div>
          <div className="flex space-x-8">
            <a href="#" className="text-slate-300 hover:text-lime-400">About</a>
            <a href="#" className="text-slate-300 hover:text-lime-400">Privacy</a>
            <a href="#" className="text-slate-300 hover:text-lime-400">Terms</a>
            <a href="#" className="text-slate-300 hover:text-lime-400">Contact</a>
          </div>
        </div>
        
      </footer>
    </section>
  );
}
