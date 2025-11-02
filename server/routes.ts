import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import multer from "multer";
import { ExcelHandler } from "./excel-handler";
import { insertEstimateSchema, insertSSRItemSchema } from "@shared/schema";
import { fromError } from "zod-validation-error";

const upload = multer({ storage: multer.memoryStorage() });

export async function registerRoutes(app: Express): Promise<Server> {
  // SSR Items endpoints
  app.get("/api/ssr-items", async (req, res) => {
    try {
      const items = await storage.getAllSSRItems();
      res.json(items);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch SSR items" });
    }
  });

  app.get("/api/ssr-items/:id", async (req, res) => {
    try {
      const item = await storage.getSSRItem(req.params.id);
      if (!item) {
        return res.status(404).json({ error: "SSR item not found" });
      }
      res.json(item);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch SSR item" });
    }
  });

  app.get("/api/ssr-items/code/:code", async (req, res) => {
    try {
      const item = await storage.getSSRItemByCode(req.params.code);
      if (!item) {
        return res.status(404).json({ error: "SSR item not found" });
      }
      res.json(item);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch SSR item" });
    }
  });

  app.get("/api/ssr-items/category/:category", async (req, res) => {
    try {
      const items = await storage.getSSRItemsByCategory(req.params.category);
      res.json(items);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch SSR items by category" });
    }
  });

  app.post("/api/ssr-items", async (req, res) => {
    try {
      const result = insertSSRItemSchema.safeParse(req.body);
      if (!result.success) {
        return res.status(400).json({ error: fromError(result.error).toString() });
      }
      
      const item = await storage.createSSRItem(result.data);
      res.status(201).json(item);
    } catch (error) {
      res.status(500).json({ error: "Failed to create SSR item" });
    }
  });

  // Estimates endpoints
  app.get("/api/estimates", async (req, res) => {
    try {
      const estimates = await storage.getAllEstimates();
      res.json(estimates);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch estimates" });
    }
  });

  app.get("/api/estimates/:id", async (req, res) => {
    try {
      const estimate = await storage.getEstimate(req.params.id);
      if (!estimate) {
        return res.status(404).json({ error: "Estimate not found" });
      }
      res.json(estimate);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch estimate" });
    }
  });

  app.post("/api/estimates", async (req, res) => {
    try {
      const result = insertEstimateSchema.safeParse(req.body);
      if (!result.success) {
        return res.status(400).json({ error: fromError(result.error).toString() });
      }
      
      const estimate = await storage.createEstimate(result.data);
      res.status(201).json(estimate);
    } catch (error) {
      res.status(500).json({ error: "Failed to create estimate" });
    }
  });

  // Excel file upload and parsing
  app.post("/api/excel/upload", upload.single("file"), async (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({ error: "No file uploaded" });
      }

      const excelData = ExcelHandler.parseExcelFile(req.file.buffer);
      const parts = ExcelHandler.findPartSheets(excelData.sheetNames);

      // Create estimate with parsed data
      const estimate = await storage.createEstimate({
        projectName: req.body.projectName || "Untitled Project",
        location: req.body.location || "",
        engineerName: req.body.engineerName || "",
        referenceNumber: req.body.referenceNumber || "",
        status: "draft",
        fileName: req.file.originalname,
        excelData: {
          sheetNames: excelData.sheetNames,
          parts: parts,
        },
      });

      res.status(201).json({
        estimate,
        sheetNames: excelData.sheetNames,
        parts,
      });
    } catch (error) {
      console.error("Excel upload error:", error);
      res.status(500).json({ error: "Failed to process Excel file" });
    }
  });

  // Insert SSR item into Excel
  app.post("/api/excel/:estimateId/insert-ssr", async (req, res) => {
    try {
      const { estimateId } = req.params;
      const { ssrItemId, partNumber, insertAtRow } = req.body;

      if (!ssrItemId || partNumber === undefined) {
        return res.status(400).json({ error: "Missing required fields" });
      }

      // Get estimate and SSR item
      const estimate = await storage.getEstimate(estimateId);
      if (!estimate) {
        return res.status(404).json({ error: "Estimate not found" });
      }

      const ssrItem = await storage.getSSRItem(ssrItemId);
      if (!ssrItem) {
        return res.status(404).json({ error: "SSR item not found" });
      }

      // Parse the Excel data from estimate
      if (!estimate.excelData) {
        return res.status(400).json({ error: "No Excel data found in estimate" });
      }

      const parts = (estimate.excelData as any).parts || [];
      const part = parts.find((p: any) => p.partNumber === partNumber);
      
      if (!part) {
        return res.status(404).json({ error: `Part ${partNumber} not found` });
      }

      // For this endpoint to fully work, we would need to store the actual Excel buffer
      // For now, return the information about what would be inserted
      res.json({
        message: "SSR item insertion prepared",
        ssrItem,
        part,
        serialNumberAssigned: insertAtRow || "auto",
        note: "Full Excel manipulation requires the original file buffer to be stored"
      });

    } catch (error) {
      console.error("SSR insertion error:", error);
      res.status(500).json({ error: "Failed to insert SSR item" });
    }
  });

  // Download Excel with SSR items
  app.get("/api/excel/:estimateId/download", async (req, res) => {
    try {
      const { estimateId } = req.params;
      const estimate = await storage.getEstimate(estimateId);
      
      if (!estimate) {
        return res.status(404).json({ error: "Estimate not found" });
      }

      // For a complete implementation, we would:
      // 1. Retrieve the stored Excel buffer
      // 2. Apply all SSR insertions
      // 3. Return the modified file
      
      res.json({
        message: "Excel download endpoint",
        estimate,
        note: "Full implementation requires file storage system"
      });

    } catch (error) {
      console.error("Excel download error:", error);
      res.status(500).json({ error: "Failed to download Excel file" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
