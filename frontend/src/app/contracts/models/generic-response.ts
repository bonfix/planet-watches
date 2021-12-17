export interface ResponseError {
  error_code:string
  error: any
  error_message:any
}
export interface GenericResponse {
  success:boolean
  error: ResponseError
  data: any
  status_code: number
  message: string
}
