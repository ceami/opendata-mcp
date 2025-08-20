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

// API 검색 결과 아이템 스키마
export const SearchApiItemSchema = z.object({
    list_id: z.number().describe("List ID of the API"),
    list_title: z.string().describe("Advanced Title of the API"),
    title: z.string().nullable().optional().describe("Title of the API"),
    org_nm: z.string().nullable().optional().describe("Organization name"),
    data_type: z.string().describe("Data type(FILE, API)"),
    score: z.number().nullable().optional().describe("Search score"),
    detail: z.object({
        title: z.string().optional().describe("Detail title of the API"),
        description: z.string().optional().describe("Detailed description of the API"),
        endpoint: z.array(z.object({
            title: z.string().optional().describe("Endpoint title"),
            description: z.string().optional().describe("Endpoint description"),
        })).optional().describe("API endpoints information"),
    }).nullable().optional().describe("Additional detail information with structured format"),
}).describe("Search API result item");

// API 검색 결과 페이지네이션 스키마
export const SearchApiPaginationSchema = z.object({
    total: z.number().describe("Total number of results"),
    page: z.number().describe("Current page number"),
    pageSize: z.number().describe("Number of items per page"),
    results: z.array(SearchApiItemSchema).describe("Array of search results"),
}).describe("Search API pagination result");

// API 검색 응답 스키마 (키워드별로 그룹화된 결과)
export const SearchApiResponseSchema = z.record(z.string(), SearchApiPaginationSchema).describe("Search API response grouped by keywords");

export const StdDocsInfoSchema = z.object({
    id: z.string().describe("ID of the standard document"),
    listId: z.number().describe("List ID of the standard document"),
    detailUrl: z.string().describe("Detail URL of the standard document"),
    markdown: z.string().describe("Markdown content of the standard document"),
    llmModel: z.string().describe("LLM model used to generate the standard document"),
    tokenCount: z.number().describe("Token count of the standard document"),
}).describe("Standard document information");