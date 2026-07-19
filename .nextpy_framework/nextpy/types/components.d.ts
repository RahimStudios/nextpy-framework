/**
 * NextPy Components TypeScript Definitions
 * Type definitions for NextPy built-in components
 */

declare namespace NextPyComponents {
  // Base component props
  interface BaseProps {
    className?: string;
    id?: string;
    style?: Record<string, any>;
    children?: any;
  }

  // Button component props
  interface ButtonProps extends BaseProps {
    variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'outline' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    loading?: boolean;
    onClick?: (event: any) => void;
    type?: 'button' | 'submit' | 'reset';
    href?: string;
    target?: string;
  }

  // Card component props
  interface CardProps extends BaseProps {
    title?: string;
    description?: string;
    footer?: any;
    shadow?: 'sm' | 'md' | 'lg' | 'xl';
    border?: boolean;
    padding?: 'sm' | 'md' | 'lg';
  }

  // Modal component props
  interface ModalProps extends BaseProps {
    isOpen: boolean;
    onClose: () => void;
    title?: string;
    size?: 'sm' | 'md' | 'lg' | 'xl';
    closeOnOverlayClick?: boolean;
    showCloseButton?: boolean;
    footer?: any;
  }

  // Form component props
  interface FormProps extends BaseProps {
    onSubmit: (data: Record<string, any>) => void | Promise<void>;
    initialValues?: Record<string, any>;
    validation?: Record<string, (value: any) => string | undefined>;
    disabled?: boolean;
  }

  // Input component props
  interface InputProps extends BaseProps {
    type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search';
    placeholder?: string;
    value?: string;
    defaultValue?: string;
    required?: boolean;
    disabled?: boolean;
    readOnly?: boolean;
    error?: string;
    label?: string;
    helperText?: string;
    onChange?: (value: string) => void;
    onBlur?: (value: string) => void;
    onFocus?: (value: string) => void;
  }

  // Layout component props
  interface LayoutProps extends BaseProps {
    title?: string;
    description?: string;
    showNavigation?: boolean;
    showFooter?: boolean;
    navigation?: any;
    footer?: any;
    sidebar?: any;
  }

  // Navigation component props
  interface NavigationProps extends BaseProps {
    items: Array<{
      label: string;
      href: string;
      active?: boolean;
    }>;
    variant?: 'horizontal' | 'vertical';
    logo?: any;
  }

  // Table component props
  interface TableProps extends BaseProps {
    data: Record<string, any>[];
    columns: Array<{
      key: string;
      label: string;
      sortable?: boolean;
      render?: (value: any, row: Record<string, any>) => any;
    }>;
    pagination?: {
      page: number;
      pageSize: number;
      total: number;
      onPageChange: (page: number) => void;
    };
    loading?: boolean;
  }

  // Alert component props
  interface AlertProps extends BaseProps {
    variant?: 'info' | 'success' | 'warning' | 'error';
    dismissible?: boolean;
    onDismiss?: () => void;
    icon?: any;
  }

  // Badge component props
  interface BadgeProps extends BaseProps {
    variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger';
    size?: 'sm' | 'md' | 'lg';
  }

  // Spinner component props
  interface SpinnerProps extends BaseProps {
    size?: 'sm' | 'md' | 'lg';
    color?: string;
  }

  // Icon component props
  interface IconProps extends BaseProps {
    name: string;
    size?: 'sm' | 'md' | 'lg' | 'xl';
    color?: string;
  }
}

// Component function declarations
declare module 'nextpy/components' {
  export function Button(props: NextPyComponents.ButtonProps): any;
  export function Card(props: NextPyComponents.CardProps): any;
  export function Modal(props: NextPyComponents.ModalProps): any;
  export function Form(props: NextPyComponents.FormProps): any;
  export function Input(props: NextPyComponents.InputProps): any;
  export function Layout(props: NextPyComponents.LayoutProps): any;
  export function Navigation(props: NextPyComponents.NavigationProps): any;
  export function Table(props: NextPyComponents.TableProps): any;
  export function Alert(props: NextPyComponents.AlertProps): any;
  export function Badge(props: NextPyComponents.BadgeProps): any;
  export function Spinner(props: NextPyComponents.SpinnerProps): any;
  export function Icon(props: NextPyComponents.IconProps): any;
}

// JSX element declarations
declare namespace JSX {
  interface IntrinsicElements {
    'nextpy-button': NextPyComponents.ButtonProps;
    'nextpy-card': NextPyComponents.CardProps;
    'nextpy-modal': NextPyComponents.ModalProps;
    'nextpy-form': NextPyComponents.FormProps;
    'nextpy-input': NextPyComponents.InputProps;
    'nextpy-layout': NextPyComponents.LayoutProps;
    'nextpy-navigation': NextPyComponents.NavigationProps;
    'nextpy-table': NextPyComponents.TableProps;
    'nextpy-alert': NextPyComponents.AlertProps;
    'nextpy-badge': NextPyComponents.BadgeProps;
    'nextpy-spinner': NextPyComponents.SpinnerProps;
    'nextpy-icon': NextPyComponents.IconProps;
  }
}

export {};
