import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/common/api/',  // 新路徑
  withCredentials: true,
})
export interface Address {
  id?: number
  code: string
  address: string
  postal_code: string
  contact_person: string
  phone: string
  note: string
}

export interface SupplierCategory {
  id: number
  name: string
  note?: string
}

export interface Currency {
  id: number
  short_name: string
  name?: string
}

export interface Supplier {
  id?: number
  code: string
  name: string
  category: number | null
  currency: number | null
  short_name?: string
  tax_type?: string
  invoice_address?: number | null
  addresses: Address[]
  // 你可以繼續補充其他欄位
}

// 廠商 CRUD
export const listSuppliers = () => api.get<Supplier[]>('suppliers/')
export const getSupplier = (id: number) => api.get<Supplier>(`suppliers/${id}/`)
export const createSupplier = (data: Supplier) => api.post('suppliers/', data)
export const updateSupplier = (id: number, data: Supplier) => api.put(`suppliers/${id}/`, data)
export const deleteSupplier = (id: number) => api.delete(`suppliers/${id}/`)

// 載入選項
export const listSupplierCategories = () => api.get<SupplierCategory[]>('supplier_categories/')
export const listCurrencies = () => api.get<Currency[]>('currencies/')
export const listAddresses = () => api.get<Address[]>('addresses/')