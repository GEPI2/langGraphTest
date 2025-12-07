import { Outlet, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Network, Database, BrainCircuit, Settings } from 'lucide-react';
import { cn } from '@/lib/utils';

const Layout = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Graph Builder', icon: Network },
    { path: '/rag', label: 'RAG Knowledge', icon: Database },
    { path: '/mcp', label: 'MCP Integration', icon: Settings },
    { path: '/finetune', label: 'Fine-tuning', icon: BrainCircuit },
  ];

  return (
    <div className="flex h-screen bg-background text-foreground">
      {/* Sidebar */}
      <div className="w-64 border-r bg-card flex flex-col">
        <div className="p-6 border-b flex items-center gap-2">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
            <LayoutDashboard className="text-primary-foreground w-5 h-5" />
          </div>
          <span className="font-bold text-lg tracking-tight">AI Platform</span>
        </div>
        
        <nav className="flex-1 p-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                  isActive 
                    ? "bg-primary text-primary-foreground" 
                    : "hover:bg-accent hover:text-accent-foreground text-muted-foreground"
                )}
              >
                <Icon size={18} />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <Outlet />
      </div>
    </div>
  );
};

export default Layout;
