import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Plus, Server, Wrench } from 'lucide-react';

const MCPDashboard = () => {
  const [servers, setServers] = useState<string[]>([]);
  const [tools, setTools] = useState<any[]>([]);
  const [newServer, setNewServer] = useState({ name: '', command: '', args: '' });

  useEffect(() => {
    fetchServers();
    fetchTools();
  }, []);

  const fetchServers = async () => {
    try {
      const res = await fetch('http://localhost:8001/mcp/servers');
      const data = await res.json();
      setServers(data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchTools = async () => {
    try {
      const res = await fetch('http://localhost:8001/mcp/tools');
      const data = await res.json();
      setTools(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleConnect = async () => {
    try {
      await fetch('http://localhost:8001/mcp/servers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newServer.name,
          command: newServer.command,
          args: newServer.args.split(' ').filter(Boolean),
        }),
      });
      alert('Server connected!');
      fetchServers();
      fetchTools();
    } catch (err) {
      console.error(err);
      alert('Connection failed');
    }
  };

  return (
    <div className="p-8 space-y-8 h-full overflow-auto">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">MCP Integration</h2>
        <p className="text-muted-foreground">Connect to external tools and data sources.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Connect Server */}
        <Card>
          <CardHeader>
            <CardTitle>Connect New Server</CardTitle>
            <CardDescription>Add a local MCP server via stdio.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Server Name</label>
              <Input 
                placeholder="e.g., local-files" 
                value={newServer.name}
                onChange={(e) => setNewServer({...newServer, name: e.target.value})}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Command</label>
              <Input 
                placeholder="e.g., npx" 
                value={newServer.command}
                onChange={(e) => setNewServer({...newServer, command: e.target.value})}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Arguments</label>
              <Input 
                placeholder="e.g., -y @modelcontextprotocol/server-filesystem ./data" 
                value={newServer.args}
                onChange={(e) => setNewServer({...newServer, args: e.target.value})}
              />
            </div>
            <Button className="w-full" onClick={handleConnect}>
              <Plus className="w-4 h-4 mr-2" />
              Connect Server
            </Button>
          </CardContent>
        </Card>

        {/* Connected Servers List */}
        <Card>
          <CardHeader>
            <CardTitle>Connected Servers</CardTitle>
            <CardDescription>Active MCP connections.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {servers.map((server) => (
                <div key={server} className="flex items-center gap-2 p-3 border rounded-md">
                  <Server className="w-4 h-4 text-green-500" />
                  <span className="font-medium">{server}</span>
                </div>
              ))}
              {servers.length === 0 && (
                <div className="text-center text-muted-foreground py-4">No servers connected.</div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Available Tools */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Available Tools</CardTitle>
            <CardDescription>Tools exposed by connected servers.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {tools.map((tool, idx) => (
                <div key={idx} className="p-4 border rounded-lg bg-muted/50">
                  <div className="flex items-center gap-2 mb-2">
                    <Wrench className="w-4 h-4 text-purple-500" />
                    <span className="font-bold">{tool.name}</span>
                  </div>
                  <p className="text-xs text-muted-foreground mb-2 line-clamp-2">{tool.description}</p>
                  <div className="text-xs px-2 py-1 bg-background rounded border inline-block">
                    @{tool.server}
                  </div>
                </div>
              ))}
              {tools.length === 0 && (
                <div className="col-span-full text-center text-muted-foreground py-8">
                  No tools available. Connect a server first.
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default MCPDashboard;
