import { sql } from "drizzle-orm";
import { pgTable, text, varchar, timestamp, integer, decimal, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const estimates = pgTable("estimates", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  projectName: text("project_name").notNull(),
  location: text("location"),
  engineerName: text("engineer_name"),
  referenceNumber: text("reference_number"),
  dateCreated: timestamp("date_created").notNull().defaultNow(),
  status: text("status").notNull().default("draft"),
  excelData: jsonb("excel_data"),
  fileName: text("file_name"),
});

export const ssrItems = pgTable("ssr_items", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  code: text("code").notNull().unique(),
  description: text("description").notNull(),
  unit: text("unit").notNull(),
  rate: decimal("rate", { precision: 10, scale: 2 }).notNull(),
  category: text("category"),
});

export const insertEstimateSchema = createInsertSchema(estimates).omit({
  id: true,
  dateCreated: true,
});

export const insertSSRItemSchema = createInsertSchema(ssrItems).omit({
  id: true,
});

export type InsertEstimate = z.infer<typeof insertEstimateSchema>;
export type Estimate = typeof estimates.$inferSelect;
export type InsertSSRItem = z.infer<typeof insertSSRItemSchema>;
export type SSRItem = typeof ssrItems.$inferSelect;
