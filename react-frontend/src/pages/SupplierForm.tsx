import React, { useEffect, useState, ChangeEvent, FormEvent } from 'react'
import {
  createSupplier,
  getSupplier,
  updateSupplier,
  listSupplierCategories,
  listCurrencies,
  listAddresses,
  Supplier,
  Address,
  SupplierCategory,
  Currency,
} from '../api/supplier'
import { useNavigate, useParams } from 'react-router-dom'

export default function SupplierForm() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const isEdit = Boolean(id)

  const [supplier, setSupplier] = useState<Supplier>({
    code: '',
    name: '',
    short_name: '',
    tax_type: '',
    category: null,
    currency: null,
    invoice_address: null,
    delivery_address: null,
    supplier_type: null,
    tax_category: '',
    uniform_number: '',
    invoice_title: '',
    responsible_person: '',
    contact_person: '',
    phone1: '',
    phone2: '',
    phone3: '',
    mobile_phone: '',
    fax: '',
    purchaser: null,
    email: '',
    website: '',
    last_purchase_date: '',
    last_return_date: '',
    price_no_tax: 0,
    price_with_tax: 0,
    addresses: [
      { code: '', address: '', postal_code: '', contact_person: '', phone: '', note: '' }
    ],
  })

  const [categories, setCategories] = useState<SupplierCategory[]>([])
  const [currencies, setCurrencies] = useState<Currency[]>([])
  const [addressesOptions, setAddressesOptions] = useState<Address[]>([])

  useEffect(() => {
    listSupplierCategories().then(res => setCategories(res.data)).catch(console.error)
    listCurrencies().then(res => setCurrencies(res.data)).catch(console.error)
    listAddresses().then(res => setAddressesOptions(res.data)).catch(console.error)
  }, [])

  useEffect(() => {
    if (isEdit && id) {
      getSupplier(Number(id)).then(res => setSupplier(res.data)).catch(console.error)
    }
  }, [id, isEdit])

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target
    setSupplier(prev => ({
      ...prev,
      [name]:
        ['category', 'currency', 'invoice_address', 'delivery_address', 'purchaser', 'supplier_type'].includes(name)
          ? value === '' ? null : Number(value)
          : value,
    }))
  }

  const handleAddressChange = (index: number, e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setSupplier(prev => {
      const newAddresses = [...prev.addresses]
      newAddresses[index] = {
        ...newAddresses[index],
        [name]: value,
      }
      return {
        ...prev,
        addresses: newAddresses,
      }
    })
  }

  const addAddress = () => {
    setSupplier(prev => ({
      ...prev,
      addresses: [...prev.addresses, { code: '', address: '', postal_code: '', contact_person: '', phone: '', note: '' }]
    }))
  }

  const removeAddress = (index: number) => {
    setSupplier(prev => ({
      ...prev,
      addresses: prev.addresses.filter((_, i) => i !== index),
    }))
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    try {
      if (isEdit && id) {
        await updateSupplier(Number(id), supplier)
      } else {
        await createSupplier(supplier)
      }
      alert('儲存成功')
      navigate('/suppliers')
    } catch (error) {
      console.error(error)
      alert('儲存失敗')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="container my-4" style={{ maxWidth: 900 }}>
      <h2 className="mb-4">{isEdit ? '編輯廠商' : '新增廠商'}</h2>

      {/* 基本資料 */}
      <fieldset className="border p-3 rounded mb-4">
        <legend>基本資料</legend>
        <div className="row g-3">
          <div className="col-md-6">
            <label htmlFor="code" className="form-label">廠商編號</label>
            <input
              id="code"
              name="code"
              className="form-control"
              value={supplier.code}
              onChange={handleChange}
              required
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="name" className="form-label">廠商名稱</label>
            <input
              id="name"
              name="name"
              className="form-control"
              value={supplier.name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="short_name" className="form-label">廠商簡稱</label>
            <input
              id="short_name"
              name="short_name"
              className="form-control"
              value={supplier.short_name || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="uniform_number" className="form-label">統一編號</label>
            <input
              id="uniform_number"
              name="uniform_number"
              className="form-control"
              value={supplier.uniform_number || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="invoice_title" className="form-label">發票抬頭</label>
            <input
              id="invoice_title"
              name="invoice_title"
              className="form-control"
              value={supplier.invoice_title || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="responsible_person" className="form-label">負責人</label>
            <input
              id="responsible_person"
              name="responsible_person"
              className="form-control"
              value={supplier.responsible_person || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="contact_person" className="form-label">聯絡人</label>
            <input
              id="contact_person"
              name="contact_person"
              className="form-control"
              value={supplier.contact_person || ''}
              onChange={handleChange}
            />
          </div>
        </div>
      </fieldset>

      {/* 聯絡方式 */}
      <fieldset className="border p-3 rounded mb-4">
        <legend>聯絡方式</legend>
        <div className="row g-3">
          <div className="col-md-6">
            <label htmlFor="email" className="form-label">電子郵件</label>
            <input
              id="email"
              name="email"
              type="email"
              className="form-control"
              value={supplier.email || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="website" className="form-label">網址</label>
            <input
              id="website"
              name="website"
              type="url"
              className="form-control"
              value={supplier.website || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="phone1" className="form-label">聯絡電話一</label>
            <input
              id="phone1"
              name="phone1"
              className="form-control"
              value={supplier.phone1 || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="phone2" className="form-label">聯絡電話二</label>
            <input
              id="phone2"
              name="phone2"
              className="form-control"
              value={supplier.phone2 || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="phone3" className="form-label">聯絡電話三</label>
            <input
              id="phone3"
              name="phone3"
              className="form-control"
              value={supplier.phone3 || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="mobile_phone" className="form-label">行動電話</label>
            <input
              id="mobile_phone"
              name="mobile_phone"
              className="form-control"
              value={supplier.mobile_phone || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="fax" className="form-label">傳真號碼</label>
            <input
              id="fax"
              name="fax"
              className="form-control"
              value={supplier.fax || ''}
              onChange={handleChange}
            />
          </div>
        </div>
      </fieldset>

      {/* 交易設定 */}
      <fieldset className="border p-3 rounded mb-4">
        <legend>交易設定</legend>
        <div className="row g-3">
          <div className="col-md-6">
            <label htmlFor="currency" className="form-label">幣別</label>
            <select
              id="currency"
              name="currency"
              className="form-select"
              value={supplier.currency ?? ''}
              onChange={handleChange}
              required
            >
              <option value="">請選擇幣別</option>
              {currencies.map(cur => (
                <option key={cur.id} value={cur.id}>{cur.short_name}</option>
              ))}
            </select>
          </div>
          <div className="col-md-6">
            <label htmlFor="tax_category" className="form-label">課稅類別</label>
            <input
              id="tax_category"
              name="tax_category"
              className="form-control"
              value={supplier.tax_category || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="price_no_tax" className="form-label">產品單價（未稅）</label>
            <input
              id="price_no_tax"
              name="price_no_tax"
              type="number"
              step="0.01"
              className="form-control"
              value={supplier.price_no_tax ?? 0}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="price_with_tax" className="form-label">產品單價（含稅）</label>
            <input
              id="price_with_tax"
              name="price_with_tax"
              type="number"
              step="0.01"
              className="form-control"
              value={supplier.price_with_tax ?? 0}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="last_purchase_date" className="form-label">最近進貨日</label>
            <input
              id="last_purchase_date"
              name="last_purchase_date"
              type="date"
              className="form-control"
              value={supplier.last_purchase_date || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="last_return_date" className="form-label">最近退貨日</label>
            <input
              id="last_return_date"
              name="last_return_date"
              type="date"
              className="form-control"
              value={supplier.last_return_date || ''}
              onChange={handleChange}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="category" className="form-label">廠商類別</label>
            <select
              id="category"
              name="category"
              className="form-select"
              value={supplier.category ?? ''}
              onChange={handleChange}
              required
            >
              <option value="">請選擇廠商類別</option>
              {categories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>
        </div>
      </fieldset>

      {/* 地址設定 */}
      <fieldset className="border p-3 rounded mb-4">
        <legend>地址設定</legend>
        <div className="row g-3">
          <div className="col-md-6">
            <label htmlFor="invoice_address" className="form-label">發票地址</label>
            <select
              id="invoice_address"
              name="invoice_address"
              className="form-select"
              value={supplier.invoice_address ?? ''}
              onChange={handleChange}
            >
              <option value="">請選擇發票地址</option>
              {addressesOptions.map(addr => (
                <option key={addr.id} value={addr.id}>{addr.address}</option>
              ))}
            </select>
          </div>
          <div className="col-md-6">
            <label htmlFor="delivery_address" className="form-label">送貨地址</label>
            <select
              id="delivery_address"
              name="delivery_address"
              className="form-select"
              value={supplier.delivery_address ?? ''}
              onChange={handleChange}
            >
              <option value="">請選擇送貨地址</option>
              {addressesOptions.map(addr => (
                <option key={addr.id} value={addr.id}>{addr.address}</option>
              ))}
            </select>
          </div>
        </div>

        {/* 地址列表 */}
        <fieldset className="border p-3 rounded mb-3 mt-4">
          <legend>地址列表</legend>
          {supplier.addresses.map((addr, i) => (
            <div
              key={i}
              className="border rounded p-3 mb-3"
              style={{ backgroundColor: '#fafafa' }}
            >
              <div className="row g-3 align-items-center">
                <div className="col-md-2">
                  <label htmlFor={`addr_code_${i}`} className="form-label">
                    代碼
                  </label>
                  <input
                    id={`addr_code_${i}`}
                    name="code"
                    className="form-control"
                    value={addr.code}
                    onChange={(e) => handleAddressChange(i, e)}
                  />
                </div>
                <div className="col-md-4">
                  <label htmlFor={`addr_address_${i}`} className="form-label">
                    地址
                  </label>
                  <input
                    id={`addr_address_${i}`}
                    name="address"
                    className="form-control"
                    value={addr.address}
                    onChange={(e) => handleAddressChange(i, e)}
                  />
                </div>
                <div className="col-md-2">
                  <label htmlFor={`addr_postal_code_${i}`} className="form-label">
                    郵遞區號
                  </label>
                  <input
                    id={`addr_postal_code_${i}`}
                    name="postal_code"
                    className="form-control"
                    value={addr.postal_code}
                    onChange={(e) => handleAddressChange(i, e)}
                  />
                </div>
                <div className="col-md-2">
                  <label htmlFor={`addr_contact_person_${i}`} className="form-label">
                    聯絡人
                  </label>
                  <input
                    id={`addr_contact_person_${i}`}
                    name="contact_person"
                    className="form-control"
                    value={addr.contact_person}
                    onChange={(e) => handleAddressChange(i, e)}
                  />
                </div>
                <div className="col-md-2">
                  <label htmlFor={`addr_phone_${i}`} className="form-label">
                    電話
                  </label>
                  <input
                    id={`addr_phone_${i}`}
                    name="phone"
                    className="form-control"
                    value={addr.phone}
                    onChange={(e) => handleAddressChange(i, e)}
                  />
                </div>
              </div>
              <div className="row mt-2 align-items-center">
                <div className="col-md-10">
                  <label htmlFor={`addr_note_${i}`} className="form-label">
                    備註
                  </label>
                  <input
                    id={`addr_note_${i}`}
                    name="note"
                    className="form-control"
                    value={addr.note}
                    onChange={(e) => handleAddressChange(i, e)}
                  />
                </div>
                <div className="col-md-2 d-flex align-items-end">
                  <button
                    type="button"
                    className="btn btn-danger w-100"
                    onClick={() => removeAddress(i)}
                  >
                    移除地址
                  </button>
                </div>
              </div>
            </div>
          ))}
          <div className="mb-3">
            <button type="button" className="btn btn-outline-primary" onClick={addAddress}>
              新增地址
            </button>
          </div>
        </fieldset>
      </fieldset>

      <button type="submit" className="btn btn-primary w-100">
        儲存
      </button>
    </form>
  )
}