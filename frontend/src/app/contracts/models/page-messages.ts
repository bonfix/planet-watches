export interface PageMessage {
  message: string;
  success: boolean;
  global: boolean;
  pages: string[]
}
export interface PageMessages {
  messages: PageMessage[]
}
