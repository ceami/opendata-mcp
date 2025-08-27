/*
 * Copyright 2025 Team Aeris
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import { z } from "zod";


export const searchApiInputSchema = {
    query: z.array(z.string().describe("Keyword string(No spaces)")).describe("Array of keywords").max(5),
    page: z.number().describe("Page number(1-based)").min(1),
    pageSize: z.number().describe("Page size").min(1).max(100),
};

export const getStdDocsInputSchema = {
    listId: z.array(z.number().describe("listId returned from search_api")).min(1).max(10).describe("Array of listId"),
};

export const BaseInfoSchema = z.object({
    host: z.string().describe("Host name of the API(No protocol or slash)"),
    base_path: z.string().describe("Base path of the API(Start with '/' as a root)"),
}).describe("Base Connection information of the API");

export const ParamSchema = z.object({
    name: z.string().describe("Name of the parameter(No spaces)"),
    value: z.string().nullable().optional().describe("Value of the parameter"),
}).describe("Parameter information of the API to fetch data, if serviceKey is required, it will be automatically filled so you need to provide empty string as a value");

export const HeaderSchema = z.object({
    name: z.string().describe("Name of the header(No spaces)"),
    prefix: z.string().describe("Prefix of the header(e.g. Infuser, Bearer)"),
    value: z.string().describe("Value of the header(Accepts string only)"),
}).describe("Header information of the API to fetch data, if serviceKey is required, it will be automatically filled so you need to provide empty string as a value and put the prefix of the header(e.g. Infuser, Bearer) in the prefix field");

export const EndpointInfoSchema = z.object({
    path: z.string().describe("Path of the API(Start with '/' as a root)"),
    method: z.enum(["GET", "POST", "PUT", "DELETE"]).describe("Method of the API Now only GET is supported"),
    params: z.array(ParamSchema).default([]).optional().describe("Parameters of the API(Check the information of ParamSchema)"),
    headers: z.array(HeaderSchema).default([]).optional().describe("Headers of the API(Check the information of HeaderSchema)"),
    body: z.record(z.string(), z.any()).optional().describe("Body of the API Not supported yet"),
}).describe("Endpoint information of the API to fetch data");

export const FetchDataInputSchema = {
    baseInfo: BaseInfoSchema,
    endpointInfo: EndpointInfoSchema,
};

// API 검색 결과 아이템 스키마
export const SearchApiItemSchema = z.object({
    listId: z.number().describe("List ID of the API"),
    listTitle: z.string().describe("Advanced Title of the API"),
    title: z.string().nullable().optional().describe("Title of the API"),
    orgNm: z.string().nullable().optional().describe("Organization name"),
    dataType: z.string().describe("Data type(FILE, API)"),
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

export const SearchApiResponseSchema = SearchApiPaginationSchema.describe("Search API response with pagination");

export const StdDocsInfoSchema = z.object({
    id: z.string().describe("ID of the standard document"),
    listId: z.number().describe("List ID of the standard document"),
    detailUrl: z.string().describe("Detail URL of the standard document"),
    markdown: z.string().describe("Markdown content of the standard document"),
    llmModel: z.string().describe("LLM model used to generate the standard document"),
    tokenCount: z.number().describe("Token count of the standard document"),
}).describe("Standard document information");