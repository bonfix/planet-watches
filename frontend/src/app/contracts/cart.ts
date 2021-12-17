import {CartProduct} from "./models/cart-product";
import {Product} from "./models/product";
import {getRawStorageItem, getStorageItem, removeStorageItem, setStorageItem, StorageItem} from "@core/utils";

export class Cart {
  products: Map<number, CartProduct> = new Map()
  cost: number = 0

  addItem(item: Product): void{
    if(this.products.has(item.id))
    {
      let existingItem = this.products.get(item.id);
      // @ts-ignore
      existingItem.selected_quantity += 1;
    }
    else
    {
      let newItem : CartProduct = {
        name: item.name,
          id:item.id,
          image: item.image,
          price: item.price,
          selected_quantity: 1
      }
      this.products.set(item.id, newItem);
    }
    this.cost += Number(item.price);
    this.saveCart();
  }

  addQuantity(id: number){
     if(this.products.has(id))
    {
      let existingItem = this.products.get(id);
      // @ts-ignore
      existingItem.selected_quantity += 1;
      // @ts-ignore
      this.cost +=  parseInt(existingItem.price);
      this.saveCart();
    }
  }

  reduceQuantity(id:number){
     if(this.products.has(id))
    {
      let existingItem = this.products.get(id);
      // @ts-ignore
      existingItem.selected_quantity -= 1;
      // @ts-ignore
      this.cost -= parseInt(existingItem.price);
      // @ts-ignore
      if(existingItem.selected_quantity <= 0)
      {
        this.products.delete(id)
      }
      this.saveCart();
    }
  }

  /**
   * Get products ordered
   */
  getProducts() {
    let order = []
    for(let [k,v] of this.products.entries()){
      let p = {
        id: v.id,
        quantity: v.selected_quantity
      }
      order.push(p)
    }
    return order;
  }

  /**
   * Clear the cart
   */
  clearCart(){
    this.products.clear()
    this.cost = 0
    removeStorageItem(StorageItem.Cart)
  }

  /**
   * Save cart
   */
  saveCart(){
    let serializedProducts = Object.fromEntries(this.products);
    setStorageItem(StorageItem.Cart, serializedProducts);
  }

  /**
   * Get saved cart
   */
  getSavedCart(){
    let deserializedProducts = getStorageItem(StorageItem.Cart);
    if(deserializedProducts)
    {
      // @ts-ignore
      this.products = new Map(Object.entries(deserializedProducts));
      this.cost = 0
      for(let [k,v] of this.products.entries()){
        this.cost += v.price * v.selected_quantity;
      }
    }
  }
}
