import { HttpEvent } from "@angular/common/http";

export interface RegistrationForm {
    username: string;
    email: string;
    password: string;
    role: string;
}

export interface RequestResponse {
    status: string;
    message: string;
}

export interface Dealer {
  user_name: string;
  email: string;
  address_payload: string;
  created_at: Date;
  id: number;
  is_deleted: boolean;
  mobile_no: number;
  profile_photo: string;
  shop_name: string;
  updated_at: Date;
  user_id: number;
  about: string;
}

export interface UploadEvent {
  originalEvent: HttpEvent<any>;
  files: File[];
}