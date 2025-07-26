const Navbar = () => {
  return (
    <nav 
      className="border-b shadow-lg"
      style={{ 
        backgroundColor: 'var(--color-bg-secondary)', 
        borderColor: 'var(--color-grey-dark)' 
      }}
    >
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-white tracking-wide">
            Fin<span style={{ color: 'var(--color-orange)' }}>Vista</span>
          </h1>
          <div className="flex items-center space-x-4">
            <div 
              className="w-8 h-8 rounded-full flex items-center justify-center" 
              style={{ background: 'linear-gradient(135deg, var(--color-orange), var(--color-orange-light))' }}
            >
              <span className="text-white text-sm font-medium">U</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;