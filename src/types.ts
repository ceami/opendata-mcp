import { z } from "zod";

export const BaseInfoSchema = z.object({
    host: z.string().describe("Host name of the API"),
    base_path: z.string().describe("Base path of the API(Start with '/' as a root)"),
}).describe("Base information of the API");

export const ParamSchema = z.object({
    name: z.string().describe("Name of the parameter"),
    value: z.string().nullable().optional().describe("Value of the parameter(Accepts string only)"),
}).describe("Parameter information");

export const HeaderSchema = z.object({
    name: z.string().describe("Name of the header"),
    prefix: z.string().describe("Prefix of the header"),
    value: z.string().describe("Value of the header(Accepts string only)"),
}).describe("Header information");

export const EndpointInfoSchema = z.object({
    path: z.string().describe("Path of the API(Start with '/' as a root)"),
    method: z.string().describe("Method of the API(GET, POST, PUT, DELETE)"),
    params: z.array(ParamSchema).default([]).optional().describe("Parameters of the API(Replace the values with corresponding values)"),
    headers: z.array(HeaderSchema).default([]).optional().describe("Headers of the API(Replace the values with corresponding values)"),
    body: z.record(z.string(), z.any()).optional().describe("Body of the API(Replace the values with corresponding values)"),
}).describe("Endpoint information of the API");

export const RequestDataSchema = z.object({
    baseInfo: BaseInfoSchema,
    endpointInfo: EndpointInfoSchema,
}).describe("Request data of the API");

export const StdDocsInfoSchema = z.object({
    id: z.string().describe("ID of the standard document"),
    listId: z.number().describe("List ID of the standard document"),
    detailUrl: z.string().describe("Detail URL of the standard document"),
    markdown: z.string().describe("Markdown content of the standard document"),
    llmModel: z.string().describe("LLM model used to generate the standard document"),
    tokenCount: z.number().describe("Token count of the standard document"),
}).describe("Standard document information");