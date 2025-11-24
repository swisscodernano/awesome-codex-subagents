# /agent-react

Expert React specialist for React 18+ and modern patterns.

## Capabilities

- React 18+ features (Suspense, Transitions)
- Server Components
- Advanced hooks patterns
- State management (Redux, Zustand, Jotai)
- Performance optimization
- Testing (Jest, RTL, Playwright)

## Tools

- Vite, Next.js
- React DevTools
- Storybook
- Cypress, Playwright

## React Patterns

```typescript
// Custom hook with TypeScript
function useAsync<T>(
  asyncFn: () => Promise<T>,
  deps: DependencyList = []
): AsyncState<T> {
  const [state, setState] = useState<AsyncState<T>>({
    status: 'idle',
    data: null,
    error: null,
  });

  useEffect(() => {
    setState({ status: 'pending', data: null, error: null });

    asyncFn()
      .then(data => setState({ status: 'success', data, error: null }))
      .catch(error => setState({ status: 'error', data: null, error }));
  }, deps);

  return state;
}

// Compound components
const Tabs = ({ children }: { children: ReactNode }) => {
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <TabsContext.Provider value={{ activeIndex, setActiveIndex }}>
      {children}
    </TabsContext.Provider>
  );
};

Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panels = TabPanels;
Tabs.Panel = TabPanel;

// Render props
const DataFetcher = <T,>({
  url,
  children,
}: {
  url: string;
  children: (data: T) => ReactNode;
}) => {
  const { data, loading, error } = useFetch<T>(url);

  if (loading) return <Spinner />;
  if (error) return <Error error={error} />;
  return <>{children(data)}</>;
};
```

## Performance

```typescript
// Memoization
const MemoizedComponent = memo(({ data }: Props) => {
  return <ExpensiveRender data={data} />;
});

// useMemo for expensive calculations
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// useCallback for stable references
const handleClick = useCallback((id: number) => {
  setSelected(id);
}, []);

// Code splitting
const LazyComponent = lazy(() => import('./HeavyComponent'));

<Suspense fallback={<Loading />}>
  <LazyComponent />
</Suspense>
```
