import Link from 'next/link'
import { useRouter } from 'next/router'

const navItems = [
  { href: '/', label: 'Dashboard', icon: '📊' },
  { href: '/settings', label: 'Configurações', icon: '⚙️' },
  { href: '/agents', label: 'Agentes', icon: '🤖' },
]

export default function Layout({ children }: { children: React.ReactNode }) {
  const router = useRouter()

  return (
    <div className="min-h-screen flex">
      <nav className="w-64 bg-white shadow-lg border-r border-gray-200">
        <div className="p-6">
          <h1 className="text-xl font-bold text-primary-700">Fitness AI Coach</h1>
          <p className="text-sm text-gray-500 mt-1">Assistente pessoal de IA</p>
        </div>
        <ul className="space-y-1 px-3">
          {navItems.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                  router.pathname === item.href
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <span>{item.icon}</span>
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
        <div className="absolute bottom-0 p-6 text-xs text-gray-400">
          v1.0.0
        </div>
      </nav>
      <main className="flex-1 p-8 overflow-y-auto">
        {children}
      </main>
    </div>
  )
}
