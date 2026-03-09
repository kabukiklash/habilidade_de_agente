/**
 * Entidade EmpresaTheme - Personalização White-Label
 * @see ESPECIFICACAO_SISTEMA.md - Personalização White-Label
 */
export type FontFamily = 'Inter' | 'Roboto' | 'Open Sans' | 'Custom';
export type LayoutDensity = 'compact' | 'comfortable' | 'spacious';
export type SidebarStyle = 'collapsed' | 'expanded' | 'hidden';
export type BorderRadius = 'none' | 'small' | 'medium' | 'large';
export type ButtonStyle = 'filled' | 'outlined' | 'mixed';
export type CardStyle = 'flat' | 'elevated' | 'bordered';
export type TableStyle = 'simple' | 'striped' | 'bordered';

export interface EmpresaTheme {
  primaryColor: string;
  secondaryColor: string;
  accentColor: string;
  logoUrl: string;
  faviconUrl: string;
  fontFamily: FontFamily;
  fontScale: number;
  layoutDensity: LayoutDensity;
  sidebarStyle: SidebarStyle;
  borderRadius: BorderRadius;
  buttonStyle: ButtonStyle;
  cardStyle: CardStyle;
  tableStyle: TableStyle;
  modulosAtivos: string[];
  featuresIA: {
    preditiva: boolean;
    copilot: boolean;
    automatizacao: boolean;
  };
  nomenclaturas: {
    lead: string;
    atendente: string;
    funil: string;
  };
}
