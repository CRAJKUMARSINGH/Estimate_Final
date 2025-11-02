import { type Estimate, type InsertEstimate, type SSRItem, type InsertSSRItem } from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  // Estimates
  getEstimate(id: string): Promise<Estimate | undefined>;
  getAllEstimates(): Promise<Estimate[]>;
  createEstimate(estimate: InsertEstimate): Promise<Estimate>;
  updateEstimate(id: string, estimate: Partial<InsertEstimate>): Promise<Estimate | undefined>;
  deleteEstimate(id: string): Promise<boolean>;
  
  // SSR Items
  getSSRItem(id: string): Promise<SSRItem | undefined>;
  getSSRItemByCode(code: string): Promise<SSRItem | undefined>;
  getAllSSRItems(): Promise<SSRItem[]>;
  getSSRItemsByCategory(category: string): Promise<SSRItem[]>;
  createSSRItem(item: InsertSSRItem): Promise<SSRItem>;
  updateSSRItem(id: string, item: Partial<InsertSSRItem>): Promise<SSRItem | undefined>;
  deleteSSRItem(id: string): Promise<boolean>;
}

export class MemStorage implements IStorage {
  private estimates: Map<string, Estimate>;
  private ssrItems: Map<string, SSRItem>;

  constructor() {
    this.estimates = new Map();
    this.ssrItems = new Map();
    this.initializeSSRData();
  }

  private initializeSSRData() {
    // Initialize with some sample SSR items
    const sampleSSRItems: InsertSSRItem[] = [
      {
        code: "SSR-001",
        description: "Excavation in all types of soil including watering, ramming and dressing complete",
        unit: "cum",
        rate: "150.00",
        category: "Earthwork",
      },
      {
        code: "SSR-002",
        description: "Plain Cement Concrete 1:4:8 (40mm nominal size) including form work, curing complete",
        unit: "cum",
        rate: "4500.00",
        category: "Concrete",
      },
      {
        code: "SSR-003",
        description: "Reinforced Cement Concrete M20 grade including form work and curing complete",
        unit: "cum",
        rate: "6800.00",
        category: "Concrete",
      },
      {
        code: "SSR-004",
        description: "Brick work in cement mortar 1:6 (1 cement: 6 sand) in super structure",
        unit: "sqm",
        rate: "580.00",
        category: "Masonry",
      },
      {
        code: "SSR-005",
        description: "Steel reinforcement for RCC work including cutting, bending, binding complete",
        unit: "kg",
        rate: "65.00",
        category: "Steel",
      },
    ];

    sampleSSRItems.forEach((item) => {
      const id = randomUUID();
      const ssrItem: SSRItem = { ...item, id };
      this.ssrItems.set(id, ssrItem);
    });
  }

  // Estimates methods
  async getEstimate(id: string): Promise<Estimate | undefined> {
    return this.estimates.get(id);
  }

  async getAllEstimates(): Promise<Estimate[]> {
    return Array.from(this.estimates.values());
  }

  async createEstimate(insertEstimate: InsertEstimate): Promise<Estimate> {
    const id = randomUUID();
    const estimate: Estimate = {
      ...insertEstimate,
      id,
      dateCreated: new Date(),
    };
    this.estimates.set(id, estimate);
    return estimate;
  }

  async updateEstimate(id: string, update: Partial<InsertEstimate>): Promise<Estimate | undefined> {
    const existing = this.estimates.get(id);
    if (!existing) return undefined;
    
    const updated: Estimate = { ...existing, ...update };
    this.estimates.set(id, updated);
    return updated;
  }

  async deleteEstimate(id: string): Promise<boolean> {
    return this.estimates.delete(id);
  }

  // SSR Items methods
  async getSSRItem(id: string): Promise<SSRItem | undefined> {
    return this.ssrItems.get(id);
  }

  async getSSRItemByCode(code: string): Promise<SSRItem | undefined> {
    return Array.from(this.ssrItems.values()).find((item) => item.code === code);
  }

  async getAllSSRItems(): Promise<SSRItem[]> {
    return Array.from(this.ssrItems.values());
  }

  async getSSRItemsByCategory(category: string): Promise<SSRItem[]> {
    return Array.from(this.ssrItems.values()).filter(
      (item) => item.category === category
    );
  }

  async createSSRItem(insertItem: InsertSSRItem): Promise<SSRItem> {
    const id = randomUUID();
    const item: SSRItem = { ...insertItem, id };
    this.ssrItems.set(id, item);
    return item;
  }

  async updateSSRItem(id: string, update: Partial<InsertSSRItem>): Promise<SSRItem | undefined> {
    const existing = this.ssrItems.get(id);
    if (!existing) return undefined;
    
    const updated: SSRItem = { ...existing, ...update };
    this.ssrItems.set(id, updated);
    return updated;
  }

  async deleteSSRItem(id: string): Promise<boolean> {
    return this.ssrItems.delete(id);
  }
}

export const storage = new MemStorage();
