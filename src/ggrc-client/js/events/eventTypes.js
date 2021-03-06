/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

/**
 *
 * @event refreshRelated
 * @type {object}
 * @property {string} type - Event name.
 * @property {string} model -  Model name.
 */
const REFRESH_RELATED = {
  type: 'refreshRelated',
};

/**
 *
 * @event saveCustomRole
 * @type {object}
 * @property {string} type - Event name.
 * @property {string} groupId - Role ID.
 */
const SAVE_CUSTOM_ROLE = {
  type: 'saveCustomRole',
};

/**
 *
 * @event rolesConflict
 * @type {object}
 * @property {string} type - Event name.
 * @property {string} groupId - Role ID.
 */
const ROLES_CONFLICT = {
  type: 'rolesConflict',
};

/**
 * Switch to tab with validation error
 * @event switchToErrorPanel
 * @type {object}
 */
const SWITCH_TO_ERROR_PANEL = {
  type: 'switchToErrorPanel',
};

/**
 * Scroll to validation error field and lint it
 * @event showInvalidField
 * @type {object}
 */
const SHOW_INVALID_FIELD = {
  type: 'showInvalidField',
};

/**
 * Set id number of tab with validation error
 * @event validationError
 * @type {object}
 */
const VALIDATION_ERROR = {
  type: 'validationError',
};

/**
 *
 * @event destinationUnmapped
 * @type {object}
 * @property {string} type - Event name.
 */
const DESTINATION_UNMAPPED = {
  type: 'destinationUnmapped',
};

/**
 * Refreshes cached Related Assessments tab
 * @event refreshRelatedAssessments
 * @type {object}
 * @property {string} type - Event name.
 */
const REFRESH_TAB_CONTENT = {
  type: 'refreshTabContent',
};

/**
 * Refreshes diff of proposals
 * @event refreshProposalDiff
 * @type {object}
 * @property {string} type - Event name.
 */
const REFRESH_PROPOSAL_DIFF = {
  type: 'refreshProposalDiff',
};

/**
 * Navigate to info-pane's tab
 * @event navigateToTab
 * @type {object}
 * @property {string} type - Event name.
 * @property {string} tabId - id of tab.
 */
const NAVIGATE_TO_TAB = {
  type: 'navigateToTab',
};

/**
 * Refreshes comments of instance
 * @event refreshProposalDiff
 * @type {object}
 * @property {string} type - Event name.
 */
const REFRESH_COMMENTS = {
  type: 'refreshComments',
};

/**
 * Notifies that related items are loaded
 * @event RELATED_ITEMS_LOADED
 * @type {object}
 * @property {string} type - Event name.
 */
const RELATED_ITEMS_LOADED = {
  type: 'RELATED_ITEMS_LOADED',
};

/**
 * Notifies that new comment created and sends its instance
 * @event COMMENT_CREATED
 * @type {object}
 * @property {string} type - Event name.
 * @property {object} comment - Created comment.
 */
const COMMENT_CREATED = {
  type: 'COMMENT_CREATED',
};

/**
 * Refreshes mappings of instance
 * @event refreshMapping
 * @type {object}
 * @property {string} type - Event name.
 * @property {string} destinationType - Type of mapped object.
 */
const REFRESH_MAPPING = {
  type: 'refreshMapping',
};

export {
  REFRESH_RELATED,
  SAVE_CUSTOM_ROLE,
  ROLES_CONFLICT,
  SWITCH_TO_ERROR_PANEL,
  SHOW_INVALID_FIELD,
  VALIDATION_ERROR,
  DESTINATION_UNMAPPED,
  REFRESH_TAB_CONTENT,
  NAVIGATE_TO_TAB,
  REFRESH_PROPOSAL_DIFF,
  REFRESH_COMMENTS,
  RELATED_ITEMS_LOADED,
  COMMENT_CREATED,
  REFRESH_MAPPING,
};
