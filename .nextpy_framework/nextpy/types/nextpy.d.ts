/**
 * NextPy Framework TypeScript Definitions
 * Provides type definitions for NextPy Python framework when used with TypeScript
 */

declare module '*.py' {
  const value: any;
  export default value;
}

declare module '*.py.jsx' {
  const value: any;
  export default value;
}

declare module '*.jsx' {
  const value: any;
  export default value;
}

// Global NextPy types
declare global {
  namespace NextPy {
    // Component types
    interface ComponentProps {
      [key: string]: any;
      children?: any;
      className?: string;
      id?: string;
    }

    // Page component types
    interface PageProps extends ComponentProps {
      title?: string;
      description?: string;
    }

    // Server-side props types
    interface ServerSidePropsContext {
      params?: Record<string, string>;
      query?: Record<string, string>;
      req?: any;
      res?: any;
    }

    interface ServerSidePropsResult<T = Record<string, any>> {
      props: T;
      revalidate?: number;
      notFound?: boolean;
      redirect?: {
        destination: string;
        permanent?: boolean;
      };
    }

    interface StaticPropsContext extends ServerSidePropsContext {}

    interface StaticPropsResult<T = Record<string, any>> extends ServerSidePropsResult<T> {}

    interface StaticPathsResult {
      paths: string[];
      fallback: boolean | 'blocking';
    }

    // API types
    interface ApiRequest {
      method: string;
      url: string;
      headers: Record<string, string>;
      query: Record<string, string>;
      body?: any;
      params?: Record<string, string>;
    }

    interface ApiResponse {
      data?: any;
      error?: string;
      status?: number;
      headers?: Record<string, string>;
    }

    // Route types
    interface Route {
      path: string;
      file_path: string;
      handler?: Function;
      is_api: boolean;
      is_dynamic: boolean;
      param_names: string[];
    }

    // Component renderer types
    interface ComponentRenderer {
      render_page(file_path: string, context?: Record<string, any>): string;
      render_api_route(file_path: string, request_data: ApiRequest): ApiResponse;
      clear_cache(file_path?: string): void;
      get_cache_stats(): {
        cache_hits: number;
        cache_misses: number;
        hit_rate_percent: number;
        cache_invalidations: number;
        module_cache_size: number;
        render_cache_size: number;
      };
    }

    // JSX types
    interface JSXElement {
      type: string;
      props: ComponentProps;
      children?: JSXElement | JSXElement[] | string;
    }

    // Configuration types
    interface Config {
      app_name?: string;
      debug?: boolean;
      database_url?: string;
      secret_key?: string;
      jwt_secret?: string;
      smtp_host?: string;
      smtp_port?: number;
      smtp_user?: string;
      smtp_password?: string;
    }

    // Hook types
    interface UseStateResult<T> {
      value: T;
      setValue: (value: T | ((prev: T) => T)) => void;
    }

    interface UseEffectResult {
      cleanup?: () => void;
    }

    // Utility types
    interface CacheOptions {
      ttl?: number;
      key?: string;
    }

    interface EmailOptions {
      to: string | string[];
      subject: string;
      html?: string;
      text?: string;
      attachments?: Array<{
        filename: string;
        content: string | any;
      }>;
    }

    interface UploadOptions {
      upload_dir: string;
      max_size?: number;
      allowed_types?: string[];
    }
  }
}

// Global function declarations
declare global {
  // Component functions
  function getServerSideProps(context: NextPy.ServerSidePropsContext): NextPy.ServerSidePropsResult;
  function getStaticProps(context: NextPy.StaticPropsContext): NextPy.StaticPropsResult;
  function getStaticPaths(): NextPy.StaticPathsResult;

  // Hook functions
  function useState<T>(initialValue: T): NextPy.UseStateResult<T>;
  function useEffect(callback: () => void | (() => void), deps?: any[]): NextPy.UseEffectResult;

  // Utility functions
  function jsx(element: string | Function, props?: NextPy.ComponentProps, ...children: any[]): NextPy.JSXElement;
  function render_jsx(element: NextPy.JSXElement): string;

  // Cache functions
  function cache<T>(key: string, value: T, options?: NextPy.CacheOptions): T;
  function getCached<T>(key: string): T | null;
  function clearCache(key?: string): void;

  // Email functions
  function sendEmail(options: NextPy.EmailOptions): Promise<void>;

  // Upload functions
  function handleUpload(file: any, options: NextPy.UploadOptions): Promise<string>;

  // Validation functions
  function validateEmail(email: string): boolean;
  function validateUrl(url: string): boolean;
  function validatePhone(phone: string): boolean;

  // Auth functions
  function createToken(userId: string, expiresIn?: number): string;
  function verifyToken(token: string): string | null;
  function hashPassword(password: string): string;
  function verifyPassword(password: string, hash: string): boolean;

  // Database functions
  function getDb(): any;
  function query(sql: string, params?: any[]): Promise<any[]>;
  function transaction(callback: (db: any) => void): Promise<void>;
}

// React-like JSX declarations
declare namespace JSX {
  interface IntrinsicElements {
    [elemName: string]: NextPy.ComponentProps;
  }

  interface ElementClass {
    render(props: NextPy.ComponentProps): NextPy.JSXElement;
  }

  interface ElementAttributesProperty {
    props: {};
  }

  interface ElementChildrenAttribute {
    children: {};
  }
}

// Module declarations for NextPy modules
declare module 'nextpy/components' {
  export function Button(props: NextPy.ComponentProps): NextPy.JSXElement;
  export function Card(props: NextPy.ComponentProps): NextPy.JSXElement;
  export function Modal(props: NextPy.ComponentProps): NextPy.JSXElement;
  export function Form(props: NextPy.ComponentProps): NextPy.JSXElement;
  export function Input(props: NextPy.ComponentProps): NextPy.JSXElement;
  export function Layout(props: NextPy.ComponentProps): NextPy.JSXElement;
}

declare module 'nextpy/utils' {
  export function cache<T>(key: string, value: T, options?: NextPy.CacheOptions): T;
  export function sendEmail(options: NextPy.EmailOptions): Promise<void>;
  export function handleUpload(file: any, options: NextPy.UploadOptions): Promise<string>;
  export function validateEmail(email: string): boolean;
  export function validateUrl(url: string): boolean;
  export function validatePhone(phone: string): boolean;
}

declare module 'nextpy/auth' {
  export function createToken(userId: string, expiresIn?: number): string;
  export function verifyToken(token: string): string | null;
  export function hashPassword(password: string): string;
  export function verifyPassword(password: string, hash: string): boolean;
}

declare module 'nextpy/db' {
  export function getDb(): any;
  export function query(sql: string, params?: any[]): Promise<any[]>;
  export function transaction(callback: (db: any) => void): Promise<void>;
}

// Configuration types
declare module 'nextpy/config' {
  const config: NextPy.Config;
  export default config;
}

// CLI types
declare namespace NextPyCLI {
  interface CreateOptions {
    name: string;
    template?: string;
    typescript?: boolean;
    tailwind?: boolean;
    eslint?: boolean;
  }

  interface DevOptions {
    port?: number;
    host?: string;
    reload?: boolean;
    debug?: boolean;
  }

  interface BuildOptions {
    out?: string;
    clean?: boolean;
  }

  interface StartOptions {
    port?: number;
    host?: string;
    workers?: number;
  }
}

// Export global types
export {};
