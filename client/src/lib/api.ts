import { SSRItem, Estimate, HierarchicalSSRItem } from "@shared/schema";

export const api = {
  // SSR Items
  async getSSRItems(): Promise<SSRItem[]> {
    const response = await fetch('/api/ssr-items');
    if (!response.ok) throw new Error('Failed to fetch SSR items');
    return response.json();
  },

  async getSSRItem(id: string): Promise<SSRItem> {
    const response = await fetch(`/api/ssr-items/${id}`);
    if (!response.ok) throw new Error('Failed to fetch SSR item');
    return response.json();
  },

  async getSSRItemsByCategory(category: string): Promise<SSRItem[]> {
    const response = await fetch(`/api/ssr-items/category/${category}`);
    if (!response.ok) throw new Error('Failed to fetch SSR items');
    return response.json();
  },

  // Hierarchical SSR Items
  async getHierarchicalSSRItems(): Promise<HierarchicalSSRItem[]> {
    const response = await fetch('/api/hierarchical-ssr-items');
    if (!response.ok) throw new Error('Failed to fetch hierarchical SSR items');
    return response.json();
  },

  async getHierarchicalSSRItem(id: string): Promise<HierarchicalSSRItem> {
    const response = await fetch(`/api/hierarchical-ssr-items/${id}`);
    if (!response.ok) throw new Error('Failed to fetch hierarchical SSR item');
    return response.json();
  },

  // SSR Files
  async getSSRFiles(): Promise<any[]> {
    const response = await fetch('/api/ssr-files');
    if (!response.ok) throw new Error('Failed to fetch SSR files');
    return response.json();
  },

  async getSSRFile(id: string): Promise<any> {
    const response = await fetch(`/api/ssr-files/${id}`);
    if (!response.ok) throw new Error('Failed to fetch SSR file');
    return response.json();
  },

  async uploadSSRFile(file: File, metadata?: { description?: string; version?: string; category?: string }): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    if (metadata?.description) formData.append('description', metadata.description);
    if (metadata?.version) formData.append('version', metadata.version);
    if (metadata?.category) formData.append('category', metadata.category);

    const response = await fetch('/api/ssr-files/upload', {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Failed to upload SSR file');
    return response.json();
  },

  async analyzeSSRFile(id: string): Promise<any> {
    const response = await fetch(`/api/ssr-files/${id}/analyze`);
    if (!response.ok) throw new Error('Failed to analyze SSR file');
    return response.json();
  },

  // Estimates
  async getEstimates(): Promise<Estimate[]> {
    const response = await fetch('/api/estimates');
    if (!response.ok) throw new Error('Failed to fetch estimates');
    return response.json();
  },

  async getEstimate(id: string): Promise<Estimate> {
    const response = await fetch(`/api/estimates/${id}`);
    if (!response.ok) throw new Error('Failed to fetch estimate');
    return response.json();
  },

  async createEstimate(data: Partial<Estimate>): Promise<Estimate> {
    const response = await fetch('/api/estimates', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create estimate');
    return response.json();
  },

  // Excel operations
  async uploadExcel(file: File, metadata: {
    projectName?: string;
    location?: string;
    engineerName?: string;
    referenceNumber?: string;
  }): Promise<{ estimate: Estimate; sheetNames: string[]; parts: any[] }> {
    const formData = new FormData();
    formData.append('file', file);
    Object.entries(metadata).forEach(([key, value]) => {
      if (value) formData.append(key, value);
    });

    const response = await fetch('/api/excel/upload', {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Failed to upload Excel file');
    return response.json();
  },

  async insertSSRToExcel(estimateId: string, data: {
    ssrItemId: string;
    partNumber: number;
    insertAtRow?: number;
  }): Promise<any> {
    const response = await fetch(`/api/excel/${estimateId}/insert-ssr`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to insert SSR item');
    return response.json();
  },
};