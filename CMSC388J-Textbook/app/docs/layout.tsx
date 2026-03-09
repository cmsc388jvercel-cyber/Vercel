import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import { baseOptions } from '@/lib/layout.shared';
import { source } from '@/lib/source';

export default function Layout({ children }: LayoutProps<'/docs'>) {
  return (
    <DocsLayout
      tree={source.pageTree}
      sidebar={{
        enabled: true,
        defaultOpenLevel: 0,
      }}
      {...baseOptions()}
    >
      {children}
    </DocsLayout>
  );
}
